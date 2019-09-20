// ==UserScript==
// @name         ExilTool
// @namespace    {{ site }}
// @version      0.2.1
// @description  try to take over the world!
// @author       You
// @include      /^https://www.exxxxile.ovh/exile/map\?g=([0-9]+)&s=([0-9]+)/
// @grant        GM.xmlHttpRequest
// @require      http://code.jquery.com/jquery-latest.js
// ==/UserScript==

(function () {
    'use strict';
    var match = window.location.href.match(/g=([0-9]+)&s=([0-9]+)/);
    var galaxy = parseInt(match[1]);
    var sector = parseInt(match[2]);

    var newPlaces = [];

    function processLoc(position, img, alliancetag, id, owner, name, rel, radar, jammer, ore, hydrocarbon, floor, space, a_ore, a_hydrocarbon, vortex_strength, frozen, parked, orbit, elements, b_ore, b_hydrocarbon) {
        var planet = null;
        if (floor !== '') {
            planet = {
                'land': floor,
                'space': space,
                'mineral': a_ore,
                'hydrocarbon': a_hydrocarbon
            };
        }

        var place = {
            'galaxy': galaxy,
            'sector': sector,
            'position': position,
            'planet': planet,
            'img': img
        };

        newPlaces.push(place);
    }

    function processSector(arr) {
        for (var i = 1; i < arr.length; i++) {
            var p = arr[i];
            processLoc(i, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[15], p[16], p[17], p[18], p[19], p[20]);
        }

        GM.xmlHttpRequest({
            url: '{{ site }}api/map/places',
            data: JSON.stringify({'places': newPlaces}),
            contentType: 'application/json',
            method: 'POST',
            headers: {
                'ApiKey': '{{ apikey }}'
            }
        });
    }

    var text = $('#mapsector').siblings('script').text();
    text = text.replace('displaySector', 'processSector');
    eval(text);
})();
