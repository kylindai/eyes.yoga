/**
 * miaowa.pro javascript utils
 */

// 获取窗口宽度
function win_width() {
    if (window.innerWidth) {   //兼容DOM
        return window.innerWidth;
    } else if ((document.body) && (document.body.clientWidth)) { //兼容IE
        return document.body.clientWidth;
    }
}

// 获取窗口高度
function win_height() {
    if (window.innerHeight) {  //兼容DOM
        return window.innerHeight;
    } else if ((document.body) && (document.body.clientHeight)) { //兼容IE
        return document.body.clientHeight;
    }
}

// 防抖延时运行
function debounce(fn, delay) {
	var timer;
	return function() {
		if (timer) {
			clearTimeout(timer);
		}
		timer = setTimeout(function() {
			fn();
		}, delay);
	}
};

// 判断字符是否是大写
String.prototype.isUpper = function () {
    return this.toUpperCase() == this;
}

// 判断字符是否是小写
String.prototype.isLower = function () {
    return this.toLowerCase() == this;
}

// 格式化字符串
function format_data(data, format) {
    if (format = 'split') {
        str = [];
        for (var i = 0; i < data.length; i++) {
            c = data.charAt(i)
            if (i > 0 && c.isUpper() && data.charAt(i - 1).isLower()) {
                str.push(' ')
            }
            str.push(c)
        }
        return str.join('')
    }
    return data;
}

function is_panel_open(panel) {
    return !$(panel).is(':hidden');
}

