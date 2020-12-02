/**
 * 正则应用
 */
var REG = /** @class */ (function () {
    function REG() {
    }
    /**
     * 判断一个字符串的长度是符合密码规定
     * 最少8位,最多16位
     */
    REG.CheckPassWardRule = function (password) {
        var reg = new RegExp("^([a-z]|[A-Z]|[0-9]){8,16}$");
        return reg.test(password);
    };
    return REG;
}());
