/**
 * 正则应用
 */
class REG{
    public constructor(){}
    /**
     * 判断一个字符串的长度是符合密码规定
     * 最少8位,最多16位
     */
    public static CheckPassWardRule(password:string):boolean{
        let reg = new RegExp("^([a-z]|[A-Z]|[0-9]){8,16}$");
        return reg.test(password);
    }
}