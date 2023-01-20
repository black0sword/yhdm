function __yh_cb_getplay_url(animation_num){
    const _base_url =  "https://www.yhdmp.cc"
    const _url = "https://www.yhdmp.cc/vp/"+animation_num+".html";
    const _rand = Math.random();
    const _getplay_url = (_url.replace(/.*\/vp\/(\d+?)-(\d+?)-(\d+?)\.html.*/, '/_getplay?aid=$1&playindex=$2&epindex=$3') + '&r=' + _rand);
    return _base_url + _getplay_url;
}