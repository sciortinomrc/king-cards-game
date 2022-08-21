$("body").on("click",async()=>{
    try{
        const req = await fetch("/api/v1/gamerooms/new",{
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