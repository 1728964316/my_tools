// 点击转换按钮
    start_cal() {
        let value = this.data.value
        let value_sort = this.data.value_sort
        let cur = this.data.cur
        if (cur === -1) {
            return
        }
        for (let i = 0; i < value.length; i++) {
            if (i === cur)
                continue
            if (value[cur] === '0') {
                value[i] = 0
                continue
            }
            value[i] = this.auxiliary_cal(value[cur], value_sort[cur], value_sort[i])
            // console.log((value[i]))
        }
        this.setData({
            value: value,
        })
    },

    // 转换过程
    auxiliary_cal(str, from, to) {
        const p = '0123456789ABCDEF'
        switch (from) {
            case 2:
                // 二转十
                if (to === 10) {
                    let result1 = ''
                    let result2 = 0
                    let flag = str.indexOf('.')
                    if (flag === -1) {
                        for (let i = str.length - 1; i >= 0; i--) {
                            let c = parseInt(str[i])
                            let index = str.length - 1 - i
                            result2 += c * Math.pow(2, index)
                        }
                    } else {
                        let Integers = 0
                        let decimals = 0
                        for (let i = 1; i + flag < str.length || flag - i >= 0; i++) {
                            let pre = flag - i >= 0 ? parseInt(str[flag - i]) : 0
                            let end = i + flag < str.length ? (str[flag + i]) : 0
                            decimals += end * Math.pow(2, i - 1)
                            Integers += pre * Math.pow(2, i - 1)
                        }
                        result1 = Integers.toString() + '.' + decimals.toString()
                    }
                    return flag === -1 ? result2 : result1
                }
                // 二转十六
                if (to === 16) {
                    let flag = str.indexOf('.')
                    //判断格式是否为'0.xxxx'
                    let temp_str = str.substring(0, str.indexOf('.'))
                    let flag1 = temp_str.length === 1 && temp_str === '0'
                    if (flag === -1 && str.length % 4 !== 0) {
                        str = '0' * (4 - str.length % 4) + str
                    }
                    if ((flag !== -1) && (str.length - 1) % 4 !== 0) {
                        let str1 = str.substring(0, flag).length
                        let str2 = str.substring(flag + 1).length
                        str = (str1 % 4 === 0 ? '' : '0' * (4 - str1 % 4)) + str
                        str = str + (str1 % 4 === 0 ? '' : '0' * (4 - (str2 - 2) % 4))
                    }
                    flag = str.indexOf('.')
                    let result = flag1 ? '0.' : ''
                    // let str1 = flag!==-1?str.substring(0, flag):str
                    // let str2 = flag!==-1?str.substring(flag + 1):''
                    let str1_num=0
                    let str2_num=0
                    let str1_index=flag!==-1?flag-1:str.length-1
                    let str2_index=flag!==-1?flag+1:str.length
                    let str1_len=0
                    let str2_len=0
                    result=flag!==-1?'.':''
                    while(true){
                        if(str1_index<0&&str2_index>=str.length){
                            break
                        }

                        if(str1_index>=0){
                            str1_num+=parseInt(str[str1_index])*Math.pow(2,str1_len%4)
                        }
                        if(str1_index===0||str1_len++%4===3){
                            result=p[str1_num]+result
                            str1_num=0
                        }
                        str1_index--
                        
                        if(flag!==-1){
                            if(str2_index<str.length){
                                str2_num+=parseInt(str[str2_index])*Math.pow(2,str2_len%4)
                            }
                            if(str2_index===str.length-1||str2_len++%4===3){
                                result=result+p[str2_num]
                                str2_num=0
                            }
                            str2_index++
                        }
                        console.log('str2_index:',str2_index,str2_num,result)

                    }

                    console.log(result)
                    return result
                }
                // 二转八
                // if (to === 8) {
                //     if (str.length % 3 !== 0)
                //         return
                //     let result = ''
                //     let temp = 0
                //     for (let i = str.length - 1; i >= 0; i--) {
                //         let c = parseInt(str[i])
                //         let index = (str.length - 1 - i) % 3
                //         temp += c * Math.pow(2, index)
                //         if (index === 2) {
                //             console.log(temp)
                //             result = p[temp] + result
                //             temp = 0
                //         }
                //
                //     }
                //     return result
                // }
                break
            case 10:
                if (to === 2) {
                    let flag = str.indexOf('.')
                    if (flag === -1) {
                        let num = parseInt(str)
                        let result = ''
                        while (num !== 0) {
                            result = (num % to).toString() + result
                            num = Math.floor(num / to)
                        }
                        return result
                    } else {
                        let result_pre = 0
                        let result_end = 0
                        let result = ''
                        let pre = str.slice(0, flag)
                        let end = str.slice(flag + 1, str.length)
                        while (pre !== 0) {
                            result = (pre % to).toString() + result
                            pre = Math.floor(pre / to)
                        }
                        result += '.'
                        while (end !== 0) {
                            result = result + (end % to).toString()
                            end = Math.floor(end / to)
                        }
                        return result
                    }

                }
                if (to === 16) {
                    let flag = str.indexOf('.')
                    if (flag === -1) {
                        let num = parseInt(str)
                        let result = ''
                        while (num !== 0) {
                            result = p[num % to] + result
                            num = Math.floor(num / to)
                        }
                        return result
                    } else {
                        let result_pre = 0
                        let result_end = 0
                        let result = ''
                        let pre = str.slice(0, flag)
                        let end = str.slice(flag + 1, str.length)
                        while (pre !== 0) {
                            result = p[pre % to] + result
                            pre = Math.floor(pre / to)
                        }
                        result += '.'
                        while (end !== 0) {
                            result = result + p[end % to]
                            end = Math.floor(end / to)
                        }
                        return result
                    }

                }
                break
            case 16:
                // 十六转二
                if (to === 2) {
                    let result = ''
                    for (let i = 0; i < str.length; i++) {
                        if (str[i] === '.') {
                            result += '.'
                            continue
                        }
                        let index = p.indexOf(str[i].toUpperCase())
                        let temp = ''
                        for (let i = 0; i < 4; i++) {
                            temp = (index % 2).toString() + temp
                            index = Math.floor(index / 2)
                        }
                        result = result + temp
                    }
                    let judge_zero = result.indexOf('1')
                    if (judge_zero !== -1) {
                        result = result.substring(judge_zero)
                    }
                    return result
                }
                // 十六转十
                if (to === 10) {
                    let flag = str.indexOf('.')

                    if (flag === -1) {
                        let result = 0
                        for (let i = str.length - 1; i >= 0; i--) {
                            let index = p.indexOf(str[i].toUpperCase())
                            let num = str.length - 1 - i
                            result += index * Math.pow(16, num)
                        }
                        return result.toString()
                    } else {
                        let Integers = 0
                        let decimals = 0
                        let result = ''
                        for (let i = 1; i + flag < str.length || flag - i >= 0; i++) {
                            let pre = flag - i >= 0 ? p.indexOf(str[flag - i].toUpperCase()) : 0
                            let end = i + flag < str.length ? p.indexOf(str[flag + i].toUpperCase()) : 0
                            decimals += end * Math.pow(16, i - 1)
                            Integers += pre * Math.pow(16, i - 1)

                        }
                        result = Integers.toString() + '.' + decimals.toString()
                        return result
                    }

                }
        }
    },
