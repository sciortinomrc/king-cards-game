$("body").on("click",async()=>{
    try{
        const demo = location.search.includes("demo=true")?"?demo=true": ""
        const req = await fetch("/api/v1/gamerooms/new"+demo,{
            method: "POST"
        })
        if (req.redirected){
            window.location.href = req.url
        }
    }
    catch(e){
        console.log(e)
    }
})

const injectSize = ()=>{
    if  ( !("ontouchstart" in document) ) return
    const doc = document.documentElement
    doc.style.setProperty("--device-height", screen.height+"px")
    doc.style.setProperty("--device-width", screen.width+"px")
}
injectSize()