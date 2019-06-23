// ==UserScript==
// @author       T3rry
// @name         115一键转存文件插件（无限制）
// @namespace    https://github.com/T3rry7f/Fake115Upload
// @version      1.02
// @description  115 一键提取一键转存
// @match        https://itunnel.top/*
// @match        https://115.com/*
// @grant        GM_xmlhttpRequest
// @grant        unsafeWindow
// @grant        GM_log
// @connect      proapi.115.com
// @connect      itunnel.top
// @require      https://greasyfork.org/scripts/5392-waitforkeyelements/code/WaitForKeyElements.js?version=115012
// ==/UserScript==

(function() {
    'use strict';

   var str=document.URL;
//  if(str == "https://itunnel.top/115upload")
//  {
//      FillUidAndKey();
//  }

 waitForKeyElements("div.file-opr", AddShareSHA1Node);
 waitForKeyElements("div.dialog-bottom", AddDownloadSha1Btn);
function FillUidAndKey()
    {
  var uploadinfo=null;
  GM_xmlhttpRequest({
  method: "GET",
  url: 'http://proapi.115.com/app/uploadinfo',
  responseType: 'json',
  onload: function(response) {
       if (response.status === 200) {
              uploadinfo = response.response;
              //alert(uploadinfo.user_id+'|'+uploadinfo.userkey);
           try
{
           document.getElementById('user_id').value=uploadinfo.user_id;
           document.getElementById('user_key').value=uploadinfo.userkey;
}
           catch(err)
{
    alert('请先登录115');
}
            } else {

              return GM_log("response.status = " + response.status);
            }
  }
});
    }

function test(info)
    {
        if(info==false){
            alert("请选择正确的文件");
            return;
        }
       var link= prompt("复制分享链接到剪贴板",info);
        if (link!=null)
{
    //copyToClipboard(link);
}
    }

function GetUserKeyParams(links){

}
function DownFileBySha1(links)
    {
        console.log(links);
        if (links=="")
          {
            alert("链接不能为空");
            return;
          }

         var uploadinfo=null;
          var cid=0;
          GM_xmlhttpRequest({
              method: "GET",
              url: 'http://proapi.115.com/app/uploadinfo',
              responseType: 'json',
              onload: function(response) {
                  if (response.status === 200) {
                      uploadinfo = response.response;
                    //  alert(uploadinfo.user_id+'|'+uploadinfo.userkey);
                     // return (uploadinfo.user_id+'|'+uploadinfo.userkey);
                      try
                      {

                          var requestParams=encodeURI("links="+links+"&uid="+uploadinfo.user_id+"&userkey="+uploadinfo.userkey+"&cid=0");
         

                          GM_xmlhttpRequest({
                              method: "GET",
                              url: 'https://itunnel.top/115uploader?'+requestParams,
                              responseType: 'text',
                              onload: function(response) {
                                  if (response.status === 200) {
                                      var uploadinfo = response.response;
                                      try
                                      {
                                          alert(uploadinfo);

                                      }
                                      catch(err)
                                      {
                                          alert(err);
                                      }
                                  } else {

                                      return GM_log("response.status = " + response.status);
                                  }
                              }
                          });
                         // return ret;
                      }
                      catch(err)
                      {
                          alert('请先登录115');
                      }
                  } else {

                      return GM_log("response.status = " + response.status);
                  }
              }
          });



    }


function GetSha1LinkByliNode(liNode)
    {
      var type=(liNode.getAttribute("file_type"));
       if(type=="0")
      {
          var fid  = liNode.getAttribute('cate_id');
          return false;
         // console.log(fid);
       }
     else
     {
         var filename  = liNode.getAttribute('title');
         var filesize =liNode.getAttribute('file_size');
          var sha1 =liNode.getAttribute('sha1');
         return (filename+'|'+filesize+'|'+sha1);

          console.log(filename+'|'+filesize+'|'+sha1);
     }
    }
function AddDownloadSha1Btn(jNode)
    {   if (document.getElementById('downsha1')==null){
        var id=document.createElement('div');
        id.setAttribute('class','con');
        id.setAttribute('id','downsha1');
         var ia=document.createElement('a');
          ia.setAttribute('class','button');
        ia.setAttribute('href','javascript:;');
         var inode=document.createTextNode("转存(sha1)");
         ia.appendChild(inode);
         id.appendChild(ia);
        jNode[0].appendChild(id);
        id.addEventListener('click', function (e) {
          var links= document.getElementById('js_offline_new_add').value
          DownFileBySha1(links);

        })
    }

    }
function AddShareSHA1Node (jNode)
    {
        var parentNode=jNode[0].parentNode;
        var sha1Link=GetSha1LinkByliNode(parentNode);
        console.log(parentNode);
        var aclass=document.createElement('a');
        aclass.addEventListener('click', function (e) {
           test(sha1Link);

        })

        var iclass=document.createElement('i');

        var ispan=document.createElement('span');

        var node=document.createTextNode("分享SHA1");

        ispan.appendChild(node);

        aclass.appendChild(iclass);
        aclass.appendChild(ispan);
        jNode[0].appendChild(aclass);

   }

})();
