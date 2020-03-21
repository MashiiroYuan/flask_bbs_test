//
//
// $(function () {
//     $("#submit").click(function (event) {
//         //阻止按钮默认提交表单时间
//         event.preventDefault();
//         var oldpwdEle=$('input[name=oldpwd]');
//         var newpwdEle=$('input[name=newpwd]');
//         var new2pwdEle=$('input[name=newpwd2]');
//         //value 获取
//         var oldpwd=oldpwdEle.val();
//         var newpwd=newpwdEle.val();
//         var new2pwd=new2pwdEle.val();
//
//         //发送 渲染csrf-token ajax请求头 设置X-csrf-token
//         zlajax.post({
//             'url':'/cms/resetpwd/',
//             'data': {
//                 'oldpwd': oldpwd,
//                 'newpwd': newpwd,
//                 'new2pwd': new2pwd
//             },
//             'success':function (data) {
//                 console.log(data);
//             },
//             'fail':function (error) {
//                 console.log(error);
//             }
//         })
//
//
//     })
//
// });
//
//


/**
 * Created by hynev on 2017/11/25.
 */

$(function () {
    $("#submit").click(function (event) {
        // event.preventDefault
        // 是阻止按钮默认的提交表单的事件
        event.preventDefault();

        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        // 1. 要在模版的meta标签中渲染一个csrf-token
        // 2. 在ajax请求的头部中设置X-CSRFtoken
        zlajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                //code 200
                console.log(data);
                if (data['code']==200){
                    zlalert.alertSuccessToast('修改成功');
                }else{
                   var message=data['message'];
                   zlalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                console.log(error);
                zlalert.alertNetworkError();
            }
        });
    });
});