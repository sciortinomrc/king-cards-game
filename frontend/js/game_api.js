const getPhase = async ()=>{
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/phase")
        if(request.status!=200) throw new Error()
        const phase = await request.json()
        return phase.phase
    }   
    catch(e){
        console.log(e)
    }
}

const getPlayerHand = async () => {
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/player/"+myself+"/cards")
        if(request.status!=200) throw new Error()
        const cards = await request.json()
        return cards.cards
    }   
    catch(e){
        console.log(e)
        return []
    }
}

const getPlayerUsable = async () => {
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/player/"+myself+"/cards/usable")
        if(request.status!=200) throw new Error()
        const cards = await request.json()
        return cards.cards
    }   
    catch(e){
        console.log(e)
        return []
    }
}

const getMiddle = async () => {
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/middle")
        if(request.status!=200) throw new Error()
        const cards = await request.json()
        return cards.middle
    }   
    catch(e){
        console.log(e)
        return []
    }
}

const start = async () => {
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/start", {
            method: "POST"
        })
        if(request.status!=200) throw new Error()
    }   
    catch(e){
        console.log(e)
    }
}

const nowPlaying = async()=>{
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/playing")
        if(request.status!=200) throw new Error()
        const response = await request.json()
        return response.playing
    }
    catch(e){
        console.log(e)
        return null
    }
}

const nowDeclaring = async()=>{
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/declaring")
        if(request.status!=200) throw new Error()
        const response = await request.json()
        return response
    }
    catch(e){
        console.log(e)
        return null
    }
}

const getTurnTimer = async() => {
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/timeout")
        if(request.status!=200) throw new Error()
        const response = await request.json()
        return response.timeout
    }
    catch(e){
        console.log(e)
        return null
    }
} 

const discard = async(card) => {
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/player/"+myself+"/discard/"+card,{
            method: "POST"
        })
        if(request.status!=200) throw new Error()
    }   
    catch(e){
        console.log(e)
        return []
    }
}

const declare = async(suite) => {
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/player/"+myself+"/declare/"+suite,{
            method: "POST"
        })
        if(request.status!=200) throw new Error()
    }   
    catch(e){
        console.log(e)
        return []
    }
}

const getPicks = async()=>{
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/picks")
        if(request.status!=200) throw new Error()
        const response = await request.json()
        return response.picks
    }
    catch(e){
        console.log(e)
        return ""
    }
}


let lastRequested = 0

const getInfo = async () =>{ 
    if (Date.now() - lastRequested < 1000) return game_info
    try{
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/player/"+myself+"/info?s="+Date.now())
        if(request.status!=200) throw new Error()
        const response = await request.json()
        return response
    }
    catch(e){
        console.log(e)
        return ""
    }
}