const fan = (hand, cfg) => {
    var options = null,
        cards;

    options = $.extend(options, readOptions(hand, 'fan'));
    if (cfg) {
        options = $.extend(options, cfg);
    }
    hand.data("fan", 'radius: ' + options.radius + '; spacing: ' + options.spacing);
    addCardImages(hand, options.cards);

    cards = hand.find("img.card");
    if (cards.length === 0) {
        return;
    }
    if (options.width) {
        cards.width(options.width);
    }
    fanCards(cards, options);
}

const addCardImages = (hand, cards) => {
    var i,
        src;
    if (!cards) {
        return;
    }
    cards = module.cardNames(cards);
    hand.empty();
    for (i = 0; i < cards.length; ++i) {
        src = "src='" + module.options.imagesUrl + cards[i] + '.svg' + "'";
        hand.append("<img class='card' " + src + ">");
    }
}

const cardNames = (cards) => {
    var i,
        name,
        names = [];
    if (typeof cards === 'string') {
        cards = cards.split(' ');
    }
    // Normalise the card names.
    for (i = 0; i < cards.length; ++i) {
        if (cards[i]) {
            name = cards[i].toString().toUpperCase();
            names.push(name);
        }
    }

    return names;
}

const readOptions =($elem, name) => {
    var v, i, len, s, options, o = {};

    options = $elem.data(name);
    options = (options || '').replace(/\s/g, '').split(';');
    for (i = 0, len = options.length; i < len; i++) {
        s = options[i].split(':');
        v = s[1];
        if (v && v.indexOf(',') >= 0) {
            o[s[0]] = v.split(',');
        } else {
            o[s[0]] = Number(v) || v;
        }
    }
    return o;
}

const fanCards = (cards, options)=> {
    var n = cards.length;
    if (n === 0) {
        return;
    }

    var width = options.width || cards[0].clientWidth || 90; // hack: for a hidden hand
    var height = cards[0].clientHeight || Math.floor(width * 1.4); // hack: for a hidden hand
    var box = {};
    var coords = calculateCoords(n, options.radius, width, height, options.fanDirection, options.spacing, box);

    var hand = $(cards[0]).parent();
    hand.width(box.width);
    hand.height(box.height);

    var i = 0;
    coords.forEach(function (coord) {
        var card = cards[i++];
        card.style.left = coord.x + "px";
        card.style.top = coord.y + "px";
        card.onmouseover = function () {
            cardSetTop(card, coord.y - 10);
        };
        card.onmouseout = function () {
            cardSetTop(card, coord.y);
        };
        var rotationAngle = Math.round(coord.angle);
        var prefixes = ["Webkit", "Moz", "O", "ms"];
        prefixes.forEach(function (prefix) {
            card.style[prefix + "Transform"] = "rotate(" + rotationAngle + "deg)" + " translateZ(0)";
        });
    });

}

const calculateCoords = (numCards, arcRadius, cardWidth, cardHeight, direction, cardSpacing, box) => {
    // The separation between the cards, in terms of rotation around the circle's origin
    var anglePerCard = Math.radiansToDegrees(Math.atan(((cardWidth * cardSpacing) / arcRadius)));

    var angleOffset = ({ "N": 270, "S": 90, "E": 0, "W": 180 })[direction];

    var startAngle = angleOffset - 0.5 * anglePerCard * (numCards - 1);

    var coords = [];
    var i;
    var minX = 99999;
    var minY = 99999;
    var maxX = -minX;
    var maxY = -minY;
    for (i = 0; i < numCards; i++) {
        var degrees = startAngle + anglePerCard * i;

        var radians = Math.degreesToRadians(degrees);
        var x = cardWidth / 2 + Math.cos(radians) * arcRadius;
        var y = cardHeight / 2 + Math.sin(radians) * arcRadius;

        minX = Math.min(minX, x);
        minY = Math.min(minY, y);
        maxX = Math.max(maxX, x);
        maxY = Math.max(maxY, y);

        coords.push({ x: x, y: y, angle: degrees + 90 });
    }

    var rotatedDimensions = Math.getRotatedDimensions(coords[0].angle, cardWidth, cardHeight);

    var offsetX = 0;
    var offsetY = 0;

    if (direction === "N") {
        offsetX = (minX * -1);
        offsetX += ((rotatedDimensions[0] - cardWidth) / 2);

        offsetY = (minY * -1);
    } else if (direction === "S") {
        offsetX = (minX * -1);
        offsetX += ((rotatedDimensions[0] - cardWidth) / 2);

        offsetY = ((minY + (maxY - minY)) * -1);
    } else if (direction === "W") {
        offsetY = (minY * -1);
        offsetY += ((rotatedDimensions[1] - cardHeight) / 2);

        offsetX = (minX * -1);
        offsetX += (cardHeight - Math.rotatePointInBox(0, 0, 270, cardWidth, cardHeight)[1]);
    } else if (direction === "E") {
        offsetY = (minY * -1);
        offsetY += ((rotatedDimensions[1] - cardHeight) / 2);

        offsetX = (arcRadius) * -1;
        offsetX -= (cardHeight - Math.rotatePointInBox(0, 0, 270, cardWidth, cardHeight)[1]);
        //offsetX -= ?????;    // HELP! Needs to line up with yellow line!
    }

    coords.forEach(function (coord) {
        coord.x += offsetX;
        coord.x = Math.round(coord.x);

        coord.y += offsetY;
        coord.y = Math.round(coord.y);

        coord.angle = Math.round(coord.angle);
    });

    box.width = coords[numCards - 1].x + cardWidth;
    box.height = coords[numCards - 1].y + cardHeight;

    return coords;
}

const cardSetTop = (card, top) => {
    card.style.top = top + "px";
}