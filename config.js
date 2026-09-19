/* 网站初始业务配置。启用管理后台后，以后台保存的配置为准。
 * 这是公开配置：不要填写密码、密钥等私密信息。
 */
window.GEEKBIRD_CONFIG = Object.freeze({
  // 实际预约平台的 HTTP(S) 链接。留空时显示“预约入口尚未开放”。
  bookingUrl: "http://mp.weixin.qq.com/mp/homepage?__biz=MzAwNjI2NzM0NQ==&hid=7&sn=454cd9a0b508d331d01e072e431437fd&scene=18#wechat_redirect",
  // 紧急联系 QQ 号，使用字符串。留空时明确显示“QQ 号暂未公布”。
  emergencyQQ: "2657698039",
});
