const injectSize = ()=>{
    if  ( !("ontouchstart" in document) ) return
    const doc = document.documentElement
    doc.style.setProperty("--device-height", screen.height+"px")
    doc.style.setProperty("--device-width", screen.width+"px")
}
injectSize()
let language = location.search.split("&").filter(p=>p.includes("lang="))[0]
language = getSupportedLanguage(language)


$("#name").prop("placeholder", messages.placeholder[language])
$("#play-btn").text(messages.play_btn[language])

$("#name").on("change",async(e)=>{
    try{
        const name = myself = e.target.value
        const request = await fetch("/api/v1/gamerooms/"+roomId+"/player/"+name,{
            method: "POST"
        })
        if (request.status!=200) throw new Error()
        $("#name-form").hide()
        showWaiting()
    }
    catch(e){
    }
})

$("#play-btn").on("click",()=>{
    $("#name").trigger("change")
})


const showWaiting = async()=>{
    $("#waiting").show()
    let stillWaiting = true
    while (stillWaiting){
        await new Promise((resolve)=>{
            setTimeout(resolve,1000)
        })
        try{
            const request = await fetch("/api/v1/gamerooms/"+roomId+"/ready")
            if(request.status==200){
                stillWaiting = false
                continue
            }
            if(request.status!=204){
                throw new Error()
            }
        }
        catch(e){
            continue
        }
    }

    startGame()
    
}

const startGame = async() =>{

    await start()
    
    const defaultPhase = {
        id: "waiting"
    }

    game_info.phase = defaultPhase
    displayMessage(game_info.phase.id, language, $("#waiting"))
    await recoursivelyGetInfo()
    while (!game_info.phase || !game_info.phase.id) {
        game_info.phase = defaultPhase
        displayMessage(game_info.phase.id, language, $("#waiting"))
        await new Promise((resolve)=>setTimeout(resolve, 1000))
    }
    $("#waiting").hide()
    setPlayers()
    playPhase()
}

const recoursivelyGetInfo = async() => {
    game_info = await getInfo()
    if (game_info.complete) {
        showComplete()
        return
    }
    setTimeout(()=>{
        recoursivelyGetInfo()
    }, 1000)
}

const setPlayers = () => {
    myUuid = game_info.player_info.uuid
    for (let i = 0 ; i<game_info.players.length; i++) {
        if (game_info.players[i].name == myself){
            const tmp = game_info.players[i]
            game_info.players[i] = game_info.players[0]
            game_info.players[0] = tmp
        }
    }
    
    for (const player of game_info.players) {
        let where = player.uuid == myUuid ? "#me" : "#others"
        const playerElement = $(`
        <div class="player-wrapper">
            <div class='player' id="player-${player.uuid}">
                <img src='https://robohash.org/${player.uuid}.png'>
                </div>
            <div class='player-points' id='p-${player.uuid}'></div>
            <div class="player-name" id='n-${player.uuid}'>${player.name}</div>
        </div>`)
        $(where).append(playerElement)
    }

    updatePlayersPoints()
}

let stopPhase = false
const playPhase = async ()=>{
    displayMessage(game_info.phase.id, language, $("#phase"))
    updatePlayersPoints()
    if(stopPhase) return
    await new Promise((resolve)=>setTimeout(resolve, 1000))
    if(game_info.complete){
        return
    }
    await declaringHand()
    renderBriscola()
    playersHand()
}


const updatePlayersPoints = () => {
    for (const player of game_info.players) {
        $("#p-"+player.uuid).text(player.points)
    }
}

const updateTimeout = () => {
    let uuid = game_info.playing
    if ( game_info.declaring ) uuid = game_info.declaring.player
    $(".player-name:not(#n-"+uuid+")").removeClass("playing").css("background", "white")
    $(".player").removeClass("playing").removeClass("med").removeClass("exp")
    $("#n-"+uuid).addClass("playing")
    $("#player-"+uuid).addClass("playing")
    const timerPercent = (game_info.timer / 45) * 100 
    let timeoutColor = "--timer-color"
    if(timerPercent>=33 && timerPercent<66) {
        timeoutColor = "--timer-color-med"
        $(".playing").addClass("med")
    }
    if(timerPercent>=66) {
        timeoutColor = "--timer-color-exp"
        $(".playing").addClass("exp")
    }

    $("#n-"+uuid).css("background", "linear-gradient(90deg, var("+timeoutColor+") "+timerPercent+"%, white 0% , white 100% ")
}


const renderBriscola  = () => {
    if(!game_info.briscola) return
    const suites = {"H": {label:"♥", color: "red"} , "D": {label:"♦", color: "red"}, "C": {label:"♣", color: "black"} ,"S": {label:"♠", color: "black"}}
    $("#players #briscola").remove()
    const suite = suites[game_info.briscola]
    const briscola = $("<div id='briscola' class='suit-"+suite.color+"'>"+suite.label+"</div>")
    $("#players").append(briscola)
}


const createTwoLines = (suites) => {
    const hCount = suites.H.length
    const cCount = suites.C.length
    const dCount = suites.D.length
    const sCount = suites.S.length

    const combinations = []


    if(hCount + cCount + dCount + sCount > 6){
        combinations.push({label: "HCds", a: [...suites.H, ...suites.C], b: [...suites.D, ...suites.S], val: Math.abs((hCount + cCount) - (dCount+sCount))}) 
        combinations.push({label: "HDcs", a: [...suites.H, ...suites.D], b: [...suites.C, ...suites.S], val: Math.abs((hCount + dCount) - (cCount+sCount))}) 
        combinations.push({label: "HScd", a: [...suites.H, ...suites.S], b: [...suites.C, ...suites.D], val: Math.abs((hCount + sCount) - (cCount+dCount))}) 
    }
    else{
        const onlyCombination = {label: "", a: [], b: []}
        if (hCount>0) { 
            onlyCombination.label+="H";
            onlyCombination.a.push(...suites.H)
        }
        if (cCount>0) { 
            onlyCombination.label+="C";
            onlyCombination.a.push(...suites.C)
        }
        if (dCount>0) { 
            onlyCombination.label+="D";
            onlyCombination.a.push(...suites.D)
        }
        if (sCount>0) { 
            onlyCombination.label+="S";
            onlyCombination.a.push(...suites.S)
        }

        combinations.push(onlyCombination)
    }

    let min = combinations[0]
    for(let i = 1; i<combinations.length; i++){
        if(combinations[i].val < min.val){
            min = combinations[i]
        }
    }

    let top = min.a, bottom = min.b;
    if(bottom.length > top.length){
        bottom = min.a
        top = min.b
    }


    if(top.length>=7){
        const extraFromTop = top.slice(7)
        for (let i = extraFromTop.length-1; i>=0; i--) {
            bottom.unshift(extraFromTop[i])
        }
    }
    
    return { top, bottom}

}

const splitBySuite = (myHand) => {
    const suites = {
        H: [],
        C: [],
        D: [],
        S: []
    }

    for (const card of myHand){
        if ( card.startsWith("H") ) suites.H.push(card)
        if ( card.startsWith("C") ) suites.C.push(card)
        if ( card.startsWith("D") ) suites.D.push(card)
        if ( card.startsWith("S") ) suites.S.push(card)
    }

    return createTwoLines(suites)
}

const createHand = (myHand, usable, playing) =>{
    if (!usable || !playing){
        usable = []
    }
    const thisHand = myHand.join("|")+usable.join("|")
    let hand = null
    if(thisHand != previousHand){
        const {top, bottom} = splitBySuite(myHand)
        hand = $(`<div id="hand"><div id="hand-top" class="fan"></div><div id="hand-bottom" class="fan"></div></div>`)
        for(const card of top){
            hand.find("#hand-top").append(`<img id="${card}" src="/cards/${card}.svg" data-card="${card}" class="card ${!usable.includes(card) || !playing?"disabled":""}">`)
        }
        for(const card of bottom){
            hand.find("#hand-bottom").append(`<img id="${card}" src="/cards/${card}.svg" data-card="${card}" class="card ${!usable.includes(card) || !playing?"disabled":""}">`)
        }
    }
    else{
        hand = $("#hand")
    }

    hand.find(".card").addClass("disabled")

    for (const card of usable) {
        hand.find("#"+card).removeClass("disabled")
    }

    if(thisHand != previousHand){
        $("#hand").replaceWith(hand)
        const spacing = getComputedStyle(document.documentElement).getPropertyValue('--fan-spacing')*1;
        cards.options.spacing = spacing
        cards.fan($("#hand-top"))
        cards.fan($("#hand-bottom"))
        previousHand = thisHand
    }
    
    return hand
}

const createMiddle = (cards) => {
    const middle = $(`<div id="middle" ></div>`)
    if(Array.isArray(cards)){
        for(const card of cards){
            middle.append(`<img src="/cards/${card}.svg" class="card disabled">`)
        }
    }
    else{
        
        const suitsConversion = {
            "H": "hearts",
            "D": "diamonds",
            "C": "clubs",
            "S": "spades"
        }
        const suits = Object.keys(cards)
        for (const suit of suits){
            const fullSuit = suitsConversion[suit]
            const suitMiddle = $(`<div id="middle-${fullSuit}" class="middle-suit"></div>`)
            const suitSeven = $(`<div id="middle-${fullSuit}-seven" class="middle-seven"></div>`)
            const suitHigher = $(`<div id="middle-${fullSuit}-higher" class="middle-higher" ></div>`)
            const suitLower = $(`<div id="middle-${fullSuit}-lower" class="middle-lower"></div>`)
            for(const card of cards[suit]){
                let cardValue = card.replace(suit,"")
                if(cardValue=="J") cardValue=11
                if(cardValue=="Q") cardValue=12
                if(cardValue=="K") cardValue=13
                if(cardValue=="A") cardValue=14

                cardValue = cardValue*1
                
                if(cardValue == 7){
                    suitSeven.append(`<img src="/cards/${card}.svg" class="card disabled">`)
                    continue
                }
                if(cardValue < 7){
                    suitLower.empty()
                    suitLower.append(`<img src="/cards/${card}.svg" class="card disabled">`)
                    continue
                }
                if(cardValue > 7){
                    suitHigher.empty()
                    suitHigher.append(`<img src="/cards/${card}.svg" class="card disabled">`)
                    continue
                }

            }
            suitMiddle.append(suitSeven)
            suitMiddle.append(suitLower)
            suitMiddle.append(suitHigher)
            middle.append(suitMiddle)
        }

    }
    return middle
}


let game_info = {phase: null};



let played = false


const terminateHand = async ()=>{
    await renderCards("not-me")
    if( phase.id!="p7" && $("#middle .card").length == 4 )
        await new Promise((resolve)=>setTimeout(resolve, 2000))
    stopPhase = true
    setTimeout(()=>{stopPhase=false; playPhase();}, 2000)
}

const doPlayHand = async () =>{
    played = false
    let playedByPlayer = false
    $(".card:not(.disabled)").off().on("click", async(e)=>{
        $(".card").off()
        await discard(e.target.dataset.card)
        await new Promise((resolve)=>setTimeout(resolve,2000))
        played = playedByPlayer = true
        terminateHand()
        
    })
    const myHand = game_info.player_info.cards
    while(!played){
        
        const myHandNow = game_info.player_info.cards
        if (myHandNow.length < myHand.length ){
            played=true
            break
        }
        updateTimeout()
        await new Promise((resolve)=>setTimeout(resolve, 1000))
    }
    
    if(!playedByPlayer) {
        terminateHand()
    }
    
}

const doDeclareHand = async () =>{
    declared = false
    let declaredByPlayer = false
    $("#declaration div:not(.disabled)").off().on("click", async(e)=>{
        stopPhase = true
        const suite = e.target.dataset.suite
        await declare(suite)
        $("#declaration").removeClass("active")
        $("#middle").show()
        declared = declaredByPlayer = true
        terminateHand()  
        setTimeout(()=>{stopPhase=false; playPhase()}, 3000)
    })
    const myHand = game_info.player_info.cards
    while(!declared){
        const myHandNow = game_info.player_info.cards
        if (myHandNow.length < myHand.length ){
            declared=true
            break
        }
        updateTimeout()
        await new Promise((resolve)=>setTimeout(resolve, 1000))
    }
    
    if(!declaredByPlayer) {
        terminateHand()
    }
    
}

const renderMiddle = async()=>{
    const middle = game_info.middle
    const thisMiddle = JSON.stringify(middle)
    if (previousMiddle != thisMiddle ){
        const middleCards = createMiddle(middle)
        $("#middle").replaceWith(middleCards)
        previousMiddle = thisMiddle
    }
}

const renderHand = async(playing) =>{
    const myHand = game_info.player_info.cards
    const usable = game_info.turn_cards
    createHand(myHand, usable, playing == myUuid)
    
}

const renderCards = async(playing)=>{
    await renderMiddle()
    await renderHand(playing)
    for (const card of [...$(".card.disabled")]){
        card.onmouseover=null
        card.onmouseout=null
    }
    $(".card[data-card*='"+game_info.briscola+"'").addClass("briscola")
    $("#play").show()
}

let previousHand = null
let previousMiddle = null


const playersHand = async () =>{
    if(game_info.declaring){
        playPhase()
        return
    }
    let playing = game_info.playing
    const myHand = game_info.player_info.cards
    updateTimeout()
    
    if (!myHand.length){
        playPhase()
        return
    }
    await renderCards(playing)
    if(playing==myUuid){
        doPlayHand()
        return
    }
    playPhase()

}

const renderDeclaration = (mustDeclare) => {
    $("#middle").hide()
    $("#declaration").addClass("active")
    if(mustDeclare){
        $("#declaration .suit-P").hide()
    }
    else{
        $("#declaration .suit-P").show()
    }
}

const declaringHand = async () =>{
    let declaring = game_info.declaring
    updateTimeout()
    if(!declaring || !declaring.player) {
        $("#declaration").removeClass("active")
        $("#middle").show()
        return
    }
    await renderCards(declaring.player)
    if(declaring.player == myUuid){
        renderDeclaration(declaring.must_declare)
        await doDeclareHand()
    }

}

const showComplete = () => {
    for (let i = 0; i < 4; i++ ) {
        const player = game_info.players[i] 
        const img = `<img src='https://robohash.org/${player.uuid}.png'></img>`
        const name = player.name
        const points = player.points
        $(".player-"+(i+1)).html(img + "<br>" + name)
        $(".points-"+(i+1)).text(points)
    }

    $("#game-wrapper > *").hide()
    $("#complete").show()
}





const search = location.search.replace("?","").split("&")
const roomId = search.filter(p=>p.includes("room"))[0].split("=")[1]
let myself = null, myUuid = null





$("#game-wrapper > div").hide()
$("#name-form").show()

if(location.search.includes("demo=true")){
    $("#game-wrapper > div").hide()
    $("#name-form").hide()
    $("#waiting").show()
    setTimeout(()=>{
        $("#name").val("Player1")
        $("#play-btn").click()
    },3000)
}