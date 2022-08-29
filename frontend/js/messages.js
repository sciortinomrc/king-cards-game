const supportedLanguages = ["it-IT", "en-US"]
const getSupportedLanguage = (lang) => {
    if(!supportedLanguages.includes(lang)){
        return "en-US"
    }
    return lang
}
const messages = {
    "waiting":{
        "en-US": "The game will start when all the players are ready...",
        "it-IT": "La partita iniziera' appena tutti i giocatori saranno pronti..."
    },
    "croupier":{
        "en-US": "The croupier is shuffling...",
        "it-IT": "Il croupier sta mescolando le carte..."
    },
    "p1":{
        "en-US": "Don't pick - -1 point for every pick",
        "it-IT": "No prese - Ogni presa -1 punto"
    },
    "p2":{
        "en-US": "Don't pick Js or Ks - -1 point for every pick",
        "it-IT": "No J o K - Ogni presa -1 punto"
    },
    "p3":{
        "en-US": "Don't pick Qs - -2 point for every pick",
        "it-IT": "No Q - Ogni presa -2 punti"
    },
    "p4":{
        "en-US": "Don't pick Hearts - -1 point for every pick",
        "it-IT": "No carte di cuori - Ogni presa -1 punto"
    },
    "p5":{
        "en-US": "Don't pick the last 2 hands - -2 point for every pick",
        "it-IT": "No ultime due prese - Ogni presa -2 punti"
    },
    "p6":{
        "en-US": "Don't pick the King of hearts - -6 points",
        "it-IT": "No K di cuori - Presa -6 punti"
    },
    "p7":{
        "en-US": "Domino - +3 winner / -1 losers",
        "it-IT": "Domino - Chi vince +3, chi perde -1"
    },
    "p8":{
        "en-US": "Briscola - +1 for every pick",
        "it-IT": "Briscola - Ogni presa +1"
    },
    "placeholder":{
        "en-US": "Type your name here",
        "it-IT": "Inserisci il tuo nome"
    },
    "play_btn":{
        "en-US": "Play",
        "it-IT": "Gioca"
    }
}

const displayMessage = (phase, language, element) => {
    console.log(phase, language)
    element.text(messages[phase][language])
}