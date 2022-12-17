
function fnDownloadLink(sURL, sFileName='') {
    const a = document.createElement('a')
    a.href = sURL
    a.download = sFileName ? sFileName : sURL.split('/').pop()
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
}