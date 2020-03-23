function CRC(){

}

/**模二加 */
function mod2_plus(a,b){
    return a | b;
    // let bi_a = a.toString(2);
    // let bi_b = b.toString(2);
    // let l_a = bi_a.length;
    // let l_b = bi_b.length;
    // let bi_min,bi_max,len;
    // if(l_a > l_b){
    //     bi_min = bi_b;
    //     bi_max = bi_a;
    //     len = l_a;
    // }else{
    //     bi_min = bi_a;
    //     bi_max = bi_b;
    //     len = l_b;
    // }
    // let concat_str = "";
    // for(let i = 0;i < Math.abs(l_a - l_b);i++){
    //     concat_str += "0";
    // }
    // bi_min = concat_str + bi_min;
    // let str = "";
    // let ret;
    // for(let i=0;i<len;i++){
    //     let byte_min = +bi_min[i];
    //     let byte_max = +bi_max[i];
    //     let char = "0"
    //     if(byte_min || byte_max)
    //         char = "1";
    //     if(byte_min && byte_max)
    //         char = "0";
    //     str += char;
    // }
    // ret = parseInt(str,2);
    // console.log(ret.toString(2));
    // return ret;
}

/**模二减 */
function mod2_sub(a,b){

}

/**模二乘 */
function mod2_multi(a,b){

}

/**模二除 */
function mod2_divide(a,b){

}
