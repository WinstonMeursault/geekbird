import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const booking = 'https://www.wjx.top/m/93277562.aspx';
const feedback = 'https://www.wjx.top/m/93298004.aspx';
const source = readFileSync(new URL('../assets/app.js', import.meta.url), 'utf8');
const configSource = readFileSync(new URL('../config.js', import.meta.url), 'utf8');

test('default reservation goes straight to the booking form', () => {
  const context = { window: {} };
  vm.runInNewContext(configSource, context);
  assert.equal(context.window.GEEKBIRD_CONFIG.bookingUrl, booking);
});

for (const file of ['index.html', 'service/index.html', 'booking/index.html']) {
  test(`${file} exposes direct booking and feedback links without an intermediate page`, () => {
    const html = readFileSync(new URL(`../${file}`, import.meta.url), 'utf8');
    const anchors = html.match(/<a\b[^>]*>/g);
    assert.ok(!anchors.some(tag => tag.includes('href="/booking/"')));
    const reservations = anchors.filter(tag => tag.includes('data-booking-platform'));
    assert.ok(reservations.length >= 3);
    assert.ok(reservations.every(tag => tag.includes(`href="${booking}"`)));
    assert.ok(anchors.some(tag => tag.includes(`href="${feedback}"`) && tag.includes('button')));
    assert.match(html, /id="booking-status"/);
  });
}

function render(bookingUrl, withStatus = true) {
  const links = Array.from({ length: 4 }, () => ({
    href: booking, attributes: {},
    removeAttribute(name) { delete this[name]; },
    setAttribute(name, value) { this.attributes[name] = value; },
  }));
  const status = { hidden: true, textContent: '' };
  const copy = { addEventListener() {} };
  const document = {
    querySelectorAll(selector) { return selector === '[data-booking-platform]' ? links : []; },
    querySelector(selector) {
      return ({ '[data-booking-platform]': links[0], '#booking-status': withStatus ? status : null,
        '[data-qq]': {}, '[data-copy-qq]': copy, '.contact': {} })[selector] || null;
    },
    addEventListener() {},
  };
  vm.runInNewContext(source, { window: { GEEKBIRD_CONFIG: { bookingUrl } }, document,
    URL, location: { origin: 'http://localhost:8080' }, matchMedia: () => ({ matches: true }) });
  return { links, status };
}

test('configuration updates every booking entry, not just the first', () => {
  const url = 'https://booking.example/new-form';
  assert.ok(render(url).links.every(link => link.href === url));
});

for (const value of ['', undefined, 'not a url', 'javascript:alert(1)', 'http://localhost:8080/booking/']) {
  test(`invalid or disabled booking (${value}) disables every entry and shows status`, () => {
    const { links, status } = render(value);
    assert.ok(links.every(link => !link.href && link.attributes['aria-disabled'] === 'true'));
    assert.equal(status.hidden, false);
    assert.match(status.textContent, /预约入口暂未开放/);
  });
}

test('missing optional status does not break contact initialization', () => {
  assert.doesNotThrow(() => render('', false));
});
