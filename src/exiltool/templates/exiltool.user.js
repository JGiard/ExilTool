// ==UserScript==
// @name         {{ name }}
// @namespace    {{ site }}
// @version      {{ version }}
// @description  try to take over the world!
// @author       You
// @match        https://www.exxxxile.ovh/exile/map*
// @match        https://www.exxxxile.ovh/exile/fleet*
// @match        https://www.exxxxile.ovh/exile/orbit*
// @grant        GM.xmlHttpRequest
// @grant        GM.setValue
// @grant        GM.getValue
// @grant        GM.log
// @require      http://code.jquery.com/jquery-latest.js
// ==/UserScript==

(async function () {
    'use strict';
    /* globals $ */
    /* globals formattime */
    /* globals GM */
    /* globals activeCategory */
    /* globals fleetList */
    const baseUrl = '{{ site }}';
    const apiKey = '{{ apikey }}';

    function now() {
        return Math.floor(new Date().getTime() / 1000);
    }

    const lastCheck = await GM.getValue('last-version-check', 0);
    if (lastCheck === 0) {
        GM.setValue('last-version-check', now());
    } else if (lastCheck < now() - 86400) {
        GM.xmlHttpRequest({
            url: baseUrl + 'api/script/version',
            method: 'GET',
            headers: {
                'ApiKey': apiKey
            },
            onload: function (data) {
                if (data.responseText !== GM.info.script.version) {
                    $('body').append(
                        $('<div/>').attr('id', 'exiltool').css({
                            'position': 'absolute',
                            'top': 0,
                            'right': 0,
                            'border': '1px solid #555',
                            'background': 'black',
                            'z-index': 200,
                            'width': '350px',
                            'display': 'flex',
                            'flex-direction': 'column',
                            'align-items': 'stretch'
                        }).append(
                            $('<a/>').text('Nouvelle version du script disponible').attr('href', baseUrl + 'exiltool.user.js').css({
                                'background': 'url(/static/exile/assets/styles/s_transparent/table/enemy.png)',
                                'padding': '2px 5px'
                            })
                        )
                    );
                } else {
                    GM.setValue('last-version-check', now());
                }
            }
        });
    }

    let mapMatch = window.location.href.match(/map\?g=([0-9]+)&s=([0-9]+)/);
    if (mapMatch) {
        let galaxy = parseInt(mapMatch[1]);
        let checkG = parseInt($('#locgalaxy').val());
        let sector = parseInt(mapMatch[2]);
        let checkS = parseInt($('#locsector').val());

        let newPlaces = [];

        // noinspection JSUnusedLocalSymbols
        function processLoc(position, img, alliancetag, id, owner, name, rel, radar, jammer, ore, hydrocarbon, floor, space, a_ore, a_hydrocarbon, vortex_strength, frozen, parked, orbit, elements, b_ore, b_hydrocarbon) {
            let planet = null;
            if (floor !== '') {
                planet = {
                    'land': floor,
                    'space': space,
                    'mineral': a_ore,
                    'hydrocarbon': a_hydrocarbon,
                    'alliance': alliancetag,
                    'owner': owner
                };
            }

            let fleets = [];
            for (let i = 1; i < orbit.length; i++) {
                fleets.push({
                    'id': orbit[i][0],
                    'name': orbit[i][1],
                    'tag': orbit[i][2],
                    'player': orbit[i][3],
                    'stance': orbit[i][4],
                    'signature': orbit[i][5]
                });
            }

            let place = {
                'galaxy': galaxy,
                'sector': sector,
                'position': position,
                'planet': planet,
                'img': img,
                'elements': elements,
                'orbit': fleets
            };

            newPlaces.push(place);
        }

        // noinspection JSUnusedLocalSymbols
        function processSector(arr) {
            for (let i = 1; i < arr.length; i++) {
                let p = arr[i];
                processLoc(i, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[15], p[16], p[17], p[18], p[19], p[20]);
            }

            let data = {
                'places': newPlaces,
                'galaxy': galaxy,
                'sector': sector
            };

            // noinspection JSUnresolvedFunction
            GM.xmlHttpRequest({
                url: baseUrl + 'api/map/places',
                data: JSON.stringify(data),
                contentType: 'application/json',
                method: 'POST',
                headers: {
                    'ApiKey': apiKey
                }
            });
        }

        let text = $('#mapsector').siblings('script').text();
        text = text.replace('displaySector', 'processSector');

        let div = $('<div/>').attr('id', 'exiltool').css({
            'position': 'absolute',
            'top': 0,
            'right': 0,
            'border': '1px solid #555',
            'background': 'black',
            'z-index': 200,
            'width': '350px',
            'display': 'flex',
            'flex-direction': 'column',
            'align-items': 'stretch',
            'height': '90px',
            'overflow': 'auto'
        });

        if (galaxy !== checkG || sector !== checkS) {
            $('body').append(div);
            div.append($('<span/>').text('update error, incorrect cooordinates'));
        }

        eval(text);
    }

    let fleetsMatch = window.location.href.match(/fleets/);
    if (fleetsMatch) {
        setTimeout(function () {
            if (activeCategory === 0) {
                // noinspection JSUnresolvedFunction
                GM.xmlHttpRequest({
                    url: baseUrl + 'api/fleets',
                    data: JSON.stringify(fleetList),
                    contentType: 'application/json',
                    method: 'POST',
                    headers: {
                        'ApiKey': apiKey
                    }
                });
            }
        }, 1000);
    }

    let orbitMatch = window.location.href.match(/orbit\?planet=([0-9]+)/);
    if (orbitMatch) {
        let planetId = parseInt(orbitMatch[1]);
        let ships = [];
        $('#orbit table').eq(1).find('tr.smallitem table tr').each(function () {
            let name = $(this).find('a b').text();
            let quantity = parseInt($(this).find('td:contains("x")').text().substr(1));
            ships.push({
                'id': name,
                'quantity': quantity
            });
        });
        // noinspection JSUnresolvedFunction
        GM.xmlHttpRequest({
            url: baseUrl + 'api/orbit/' + planetId,
            data: JSON.stringify(ships),
            contentType: 'application/json',
            method: 'POST',
            headers: {
                'ApiKey': apiKey
            }
        });
    }

    let orbitsMatch = window.location.href.match(/orbits/);
    if (orbitsMatch) {
        let orbits = [];
        $('#page form div').each(function () {
            let planetId = parseInt($(this).attr('id').substr(5));
            let ships = [];
            $(this).find('table').eq(1).find('tr.smallitem table tr').each(function () {
                let name = $(this).find('a b').text();
                let quantity = parseInt($(this).find('td:contains("x")').text().substr(1));
                ships.push({
                    'id': name,
                    'quantity': quantity
                });
            });
            orbits.push({
                'planetId': planetId,
                'ships': ships
            });
        });
        // noinspection JSUnresolvedFunction
        GM.xmlHttpRequest({
            url: baseUrl + 'api/orbits',
            data: JSON.stringify(orbits),
            contentType: 'application/json',
            method: 'POST',
            headers: {
                'ApiKey': apiKey
            }
        });
    }

    const sectorDistance = 21600000;
    const planetDistance = 3600000;

    class Position {
        constructor(g, s, p) {
            this.g = g;
            this.s = s;
            this.p = p;
        }

        toString() {
            return this.g + '.' + this.s + '.' + this.p;
        }

        id() {
            return (this.g - 1) * 99 + (this.s - 1) * 25 + this.p - 1;
        }

        static distance(a, b) {
            if (a.s === b.s) {
                let dx = Math.abs((a.p - 1) % 5 - (b.p - 1) % 5);
                let dy = Math.abs(Math.floor((a.p - 1) / 5) - Math.floor((b.p - 1) / 5));
                return Math.floor(Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2)) * planetDistance);
            } else {
                let dx = Math.abs((a.s - 1) % 10 - (b.s - 1) % 10);
                let dy = Math.abs(Math.floor((a.s - 1) / 10) - Math.floor((b.s - 1) / 10));
                return Math.floor(Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2)) * sectorDistance);
            }
        }

        static compare(a, b) {
            return a.id() - b.id();
        }

        static parse(position) {
            return new Position(position.g, position.s, position.p);
        }
    }

    class Fleet {
        constructor(id, name, speed, position, destination, ready, moving, arrivalTime) {
            this.id = id;
            this.name = name;
            this.speed = speed;
            this.position = position;
            this.destination = destination;
            this.ready = ready;
            this.moving = moving;
            this.arrivalTime = arrivalTime;
        }

        timeTo(destination) {
            return Math.floor(Position.distance(this.position, destination) / this.speed);
        }

        flyTime(destination) {
            if (this.moving) {
                return this.remainingTime()
            } else {
                return this.timeTo(destination);
            }
        }

        remainingTime() {
            return this.arrivalTime - now();
        }

        static timeToCompare(destination) {
            return function (a, b) {
                return a.flyTime(destination) - b.flyTime(destination);
            }
        }

        static parse(fleet) {
            let position = fleet.position ? Position.parse(fleet.position) : null;
            let destination = fleet.destination ? Position.parse(fleet.destination) : null;
            return new Fleet(fleet.id, fleet.name, fleet.speed, position, destination, fleet.ready, fleet.moving, fleet.arrivalTime);
        }
    }

    class State {
        constructor(fleets, ongoing, destination) {
            this.fleets = fleets;
            this.ongoing = ongoing;
            this.destination = destination;
        }

        getFleet(id) {
            return this.fleets.filter(x => x.id === id)[0];
        }

        removeFleet(id) {
            this.fleets = this.fleets.filter(x => x.id !== id);
        }

        replaceFleet(fleet) {
            let oldFleet = this.getFleet(fleet.id);
            if (!oldFleet) {
                this.fleets.push(fleet);
            } else {
                let index = this.fleets.indexOf(oldFleet);
                this.fleets.splice(index, 1, fleet);
            }
        }

        sortedFleets() {
            return this.fleets.sort(Fleet.timeToCompare(this.destination)).reverse();
        }

        nextToStart() {
            return this.sortedFleets().filter(x => !x.moving)[0];
        }

        targetTime() {
            if (this.ongoing) {
                return this.sortedFleets().filter(x => x.moving).reverse()[0].flyTime(this.destination)
            }
            return this.sortedFleets()[0].flyTime(this.destination);
        }

        started() {
            return this.fleets.filter(x => x.moving).length > 0;
        }

        static parse(state) {
            return new State(
                state.fleets.map(Fleet.parse),
                state.ongoing,
                state.destination ? Position.parse(state.destination) : null
            );
        }
    }

    class StateManager {
        constructor(fleet, onrefresh, readycheck) {
            this.fleet = fleet;
            this.disconnected = false;
            this.state = new State([fleet], false, null);
            this.refresh = onrefresh;
            this.readycheck = readycheck;
            this.getStateId = 0;
            this.channel = new BroadcastChannel('synchro');
            this.channel.onmessage = (function (e) {
                // noinspection JSPotentiallyInvalidUsageOfClassThis
                this.onMessage(e);
            }).bind(this);
        }

        init() {
            this.getStateId = Math.floor(Math.random() * 10000);
            this.channel.postMessage({
                cmd: 'get-state',
                id: this.getStateId
            });
            this.refresh();
        }

        sendState() {
            GM.log('sending state : ' + JSON.stringify(this.state));
            this.channel.postMessage({
                cmd: 'update-state',
                state: this.state
            });
        }

        updateFleet() {
            this.channel.postMessage({
                cmd: 'update-fleet',
                fleet: this.fleet
            });
        }

        onMessage(e) {
            if (this.disconnected) {
                return;
            }
            if (e.data.cmd === 'get-state' && e.data.id !== this.getStateId) {
                this.channel.postMessage({
                    cmd: 'reply-state',
                    id: e.data.id,
                    state: this.state
                });
            }
            if (e.data.cmd === 'reply-state' && e.data.id === this.getStateId) {
                this.state = State.parse(e.data.state);
                this.state.replaceFleet(this.fleet);
                this.checkFleetReady();
                this.updateFleet();
                this.refresh();
            }
            if (e.data.cmd === 'update-state') {
                this.state = State.parse(e.data.state);
                this.refresh();
            }
            if (e.data.cmd === 'update-fleet') {
                this.state.replaceFleet(Fleet.parse(e.data.fleet));
                this.refresh();
            }
            if (e.data.cmd === 'check-ready') {
                this.state = State.parse(e.data.state);
                let changed = this.checkFleetReady();
                if (changed) {
                    this.updateFleet();
                }
                this.refresh();
            }
            if (e.data.cmd === 'disconnect' && e.data.id === this.fleet.id) {
                this.disconnected = true;
                this.refresh();
            }
        }

        checkFleetReady() {
            if (this.disconnected) {
                return;
            }
            let isReady = this.readycheck();
            if (this.fleet.ready !== isReady) {
                this.fleet.ready = isReady;
                this.state.replaceFleet(this.fleet);
                return true;
            }
            return false;
        }

        updateReady() {
            let changed = this.checkFleetReady();
            if (changed) {
                this.updateFleet();
            }
            this.refresh();
        }

        removeFleet(id) {
            this.state.removeFleet(id);
            if (id === this.fleet.id) {
                this.disconnected = true;
                this.refresh();
            } else {
                this.channel.postMessage({
                    cmd: 'disconnect',
                    id: id
                });
            }
            this.sendState();
            this.refresh();
        }

        initSynchro(destination) {
            this.state.ongoing = true;
            this.state.destination = destination;
            this.checkFleetReady();
            this.channel.postMessage({
                cmd: 'check-ready',
                state: this.state
            });
            this.refresh();
        }

        reconnect() {
            this.disconnected = false;
            this.state = new State();
            this.init();
        }
    }

    function parseTime(time) {
        let match = time.match(/([0-9]+)?j*\s*([0-9]{2}):([0-9]{2}):([0-9]{2})/);
        let days = match[1] ? parseInt(match[1]) : 0;
        return days * 86400 + parseInt(match[2]) * 3600 + parseInt(match[3]) * 60 + parseInt(match[4]);
    }

    let fleetMatch = window.location.href.match(/fleet\?(.*)id=([0-9]+)/);
    if (fleetMatch) {
        let opened = await GM.getValue('synchro-tool-opened', true);
        let sound = await GM.getValue('synchro-tool-sound', true);
        let panel, content, openclose, soundIcon;
        let destG = $('input[name="g"]');
        let destS = $('input[name="s"]');
        let destP = $('input[name="p"]');
        let notified = false;
        let pageTitle = document.title;

        function inputDestination() {
            return new Position(
                parseInt(destG.val()),
                parseInt(destS.val()),
                parseInt(destP.val())
            );
        }

        function setContent() {
            if (opened) {
                panel.append(content);
                openclose.text('réduire');
            } else {
                content.remove();
                openclose.text('agrandir');
            }
        }
        function setSound() {
            if (sound) {
                soundIcon.attr('class', 'fas fa-volume-up');
            } else {
                soundIcon.attr('class', 'fas fa-volume-mute');
            }
        }

        let myFleet = new Fleet(
            parseInt(fleetMatch[2]),
            $('input[name="newname"]').val() || $('#renameref').text().trim(),
            parseInt($('td:contains("Vitesse de la flotte")').siblings('td').text()),
            null,
            null,
            false,
            false,
            0
        );

        $('head').append($('<script/>').attr('src', 'https://kit.fontawesome.com/4ccc721273.js').attr('crossorigin', 'anonymous'));
        let action = $('td:contains("Action")').siblings('td').eq(0);
        if (action.text().includes('En patrouille')) {
            myFleet.moving = false;
            let posMatch = action.find('a').text().match(/([0-9]+)\.([0-9]+)\.([0-9]+)/);
            myFleet.position = new Position(parseInt(posMatch[1]), parseInt(posMatch[2]), parseInt(posMatch[3]));
        } else if (action.text().includes('En transit')) {
            myFleet.moving = true;
            let posMatch = action.find('a:contains("(")').eq(0).text().match(/([0-9]+)\.([0-9]+)\.([0-9]+)/);
            myFleet.position = new Position(parseInt(posMatch[1]), parseInt(posMatch[2]), parseInt(posMatch[3]));
            posMatch = action.find('a:contains("(")').eq(1).text().match(/([0-9]+)\.([0-9]+)\.([0-9]+)/);
            myFleet.destination = new Position(parseInt(posMatch[1]), parseInt(posMatch[2]), parseInt(posMatch[3]));
            for (let i = 0; i < 10; i++) {
                let text = action.find('#cntdwn' + i).text();
                if (text) {
                    myFleet.arrivalTime = now() + parseTime(text);
                    break;
                }
            }
        }

        function initPanel() {
            openclose = $('<a/>').attr('href', '#').css({
                'font-weight': 'bold',
            });
            soundIcon = $('<i/>').css({
                'cursor': 'pointer',
                'margin-left': 'auto',
                'margin-right': '1em',
                'align-self': 'center'
            });
            content = $('<div/>').css({
                'border-top': '1px solid #555'
            });

            panel = $('<div/>').attr('id', 'exiltool')
                .css({
                    'position': 'absolute',
                    'top': 0,
                    'right': 0,
                    'border': '1px solid #555',
                    'background': 'url(/static/exile/assets/styles/s_transparent/table/background.png)',
                    'z-index': 100,
                    'width': '350px',
                    'display': 'flex',
                    'flex-direction': 'column',
                    'align-items': 'stretch'
                }).append(
                    $('<div/>').text('Outil de synchro').css({
                        'background': 'url(/static/exile/assets/styles/s_transparent/table/title.png)',
                        'padding': '2px 5px',
                        'display': 'flex'
                    }).append(soundIcon, openclose),
                    content
                );

            openclose.click(function () {
                opened = !opened;
                setContent();
                GM.setValue('synchro-tool-opened', opened);
                return false;
            });
            soundIcon.click(function() {
                sound = !sound;
                setSound();
                GM.setValue('synchro-tool-sound', sound);
                return false;
            });

            $('body').append(panel);
        }

        initPanel();
        setContent();

        let manager;

        function refreshPanel() {
            content.empty();
            if (manager.disconnected) {
                displayReconnect();
            } else if (!manager.state.ongoing) {
                displayCreateSynchro();
            } else {
                displaySynchro();
            }
        }

        function isReady() {
            return manager.fleet.moving || manager.state.ongoing && Position.compare(inputDestination(), manager.state.destination) === 0;
        }

        manager = new StateManager(myFleet, refreshPanel, isReady);

        function displaySynchro() {
            content.append(
                $('<div/>').css({
                    'display': 'flex',
                    'justify-content': 'space-between',
                    'padding': '2px 5px'
                }).append(
                    $('<div/>').text('destination')
                ).append(
                    $('<div/>').text(manager.state.destination)
                )
            );

            content.append(
                $('<div/>').text('Flottes en synchro').css({
                    'background': 'url(/static/exile/assets/styles/s_transparent/table/title.png)',
                    'padding': '2px 5px',
                    'border-top': '1px solid #555',
                    'border-bottom': '1px solid #555'
                })
            );

            manager.state.sortedFleets().forEach(function (fleet) {
                let timeLeft = fleet.moving ? fleet.remainingTime() : fleet.timeTo(manager.state.destination);
                let deleteLink = $('<a/>').html('&times;').attr('href', '#').css('margin-left', '0.5em');
                let fleetdiv = $('<div/>').css({
                    'display': 'flex',
                    'justify-content': 'space-between',
                    'padding': '2px 5px'
                }).append(
                    $('<div/>').text(fleet.name),
                    deleteLink
                ).append(
                    $('<div/>').attr('id', 'fleet-' + fleet.id).text(timeDisplay(timeLeft)).css({
                        'text-align': 'right',
                        'flex-grow': 2
                    })
                );
                if (!fleet.ready) {
                    fleetdiv.css('background', 'url(/static/exile/assets/styles/s_transparent/table/enemy.png)');
                }
                content.append(fleetdiv);
                deleteLink.click(function () {
                    manager.removeFleet(fleet.id);
                    return false;
                });
            });

            content.append(
                $('<div/>').text('Status flotte ' + name).css({
                    'background': 'url(/static/exile/assets/styles/s_transparent/table/title.png)',
                    'padding': '2px 5px',
                    'border-top': '1px solid #555',
                    'border-bottom': '1px solid #555'
                })
            );


            if (manager.fleet.moving) {
                if (Position.compare(manager.fleet.destination, manager.state.destination) === 0) {
                    content.append(
                        $('<div/>').text('En route').css({
                            'padding': '2px 5px'
                        })
                    );
                } else {
                    content.append(
                        $('<div/>').text('Mauvaise destiation').css({
                            'background': 'url(/static/exile/assets/styles/s_transparent/table/enemy.png)',
                            'padding': '2px 5px'
                        })
                    );
                }
            } else if (!isReady()) {
                content.append(
                    $('<div/>').text('Coordonnées incorrectes').css({
                        'background': 'url(/static/exile/assets/styles/s_transparent/table/enemy.png)',
                        'padding': '2px 5px'
                    })
                )
            } else if (manager.state.nextToStart().id === manager.fleet.id && !manager.state.started()) {
                content.append(
                    $('<div/>').text('Prête à partir').css({
                        'background': 'url(/static/exile/assets/styles/s_transparent/table/pna.png)',
                        'padding': '2px 5px'
                    })
                );
            } else {
                if (!manager.state.started()) {
                    content.append(
                        $('<div/>').text('En attente du départ').css({
                            'padding': '2px 5px'
                        })
                    );
                } else {
                    let targetTime = manager.state.targetTime();
                    let arrivalTime = manager.fleet.timeTo(manager.state.destination);
                    let textDiv = $('<div/>').attr('id', 'departtext').text('Départ dans');
                    let containerDiv = $('<div/>').attr('id', 'mycontainer').css({
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'padding': '2px 5px'
                    }).append(textDiv);
                    let countdown = $('<div/>').attr('id', 'mycountdown').text(formattime(targetTime - arrivalTime));
                    containerDiv.append(countdown);
                    content.append(containerDiv);
                }
            }
        }

        function timeDisplay(remainingTime) {
            let arrivalDate = new Date((now() + remainingTime) * 1000);
            let arrivalStr = ('0' + arrivalDate.getHours()).slice(-2) + 'h' + ('0' + arrivalDate.getMinutes()).slice(-2) + ' ' + ('0' + arrivalDate.getSeconds()).slice(-2) + 's';
            return formattime(remainingTime) + ' (à ' + arrivalStr + ')';
        }

        function updateTime() {
            manager.state.fleets.forEach(function (fleet) {
                let remaining = fleet.moving ? fleet.remainingTime() : fleet.timeTo(manager.state.destination);
                let text = timeDisplay(remaining);
                if (fleet.moving) {
                    text = '▶️ ' + text;
                }
                $('#fleet-' + fleet.id).text(text);
            });
            let fleet = manager.fleet;
            if (fleet.moving) {
                return;
            }
            let targetTime = manager.state.targetTime();
            let arrivalTime = manager.fleet.timeTo(manager.state.destination);
            let myTimeLeft = targetTime - arrivalTime;
            if (myTimeLeft < 0) {
                myTimeLeft = -myTimeLeft;
                $('#departtext').text('Retard de');
                if (myTimeLeft > 10) {
                    $('#mycontainer').css('background', 'url(/static/exile/assets/styles/s_transparent/table/enemy.png)');
                }
            } else {
                if (myTimeLeft < 60) {
                    $('#mycontainer').css('background', 'url(/static/exile/assets/styles/s_transparent/table/pna.png)');
                    if (myTimeLeft <= 10 && !notified) {
                        new Notification('La flotte `' + manager.fleet.name + '` partira dans 10s', {'icon': '/static/exile/assets/reports/400.jpg'});
                        if (sound) {
                            new Audio(baseUrl + 'static/notification.ogg').play();
                        }
                        document.title = '❗️' + pageTitle;
                        notified = true;
                    } else if (myTimeLeft > 10) {
                        document.title = '🚀' + pageTitle;
                    }
                }
            }
            $('#mycountdown').text(formattime(myTimeLeft));
        }

        let createSynchroLink = $('<a/>').attr('href', '#').css('margin', '2px 5px');

        function updateLink() {
            createSynchroLink.text('Créer une synchro vers ' + destG.val() + '.' + destS.val() + '.' + destP.val());
        }

        function displayCreateSynchro() {
            updateLink();
            content.append(createSynchroLink);
            createSynchroLink.click(function () {
                manager.initSynchro(inputDestination());
                return false;
            });
        }

        destG.on('input', updateLink).on('input', function() {manager.updateReady()});
        destS.on('input', updateLink).on('input', function() {manager.updateReady()});
        destP.on('input', updateLink).on('input', function() {manager.updateReady()});
        $('select[name="planetlist"]').on('change', updateLink).on('change', manager.updateReady);

        function displayReconnect() {
            let reconnect = $('<a/>').text('Reconnecter').attr('href', '#');
            content.append(
                $('<div/>').append(
                    $('<span/>').text('Cette flotte a été déconnectée de la synchro - '),
                    reconnect
                ).css({
                    'margin': '2px 5px'
                })
            );
            reconnect.click(function () {
                manager.reconnect();
                return false;
            });
        }

        function init() {
            setContent();
            setSound();
            manager.init();
            setInterval(updateTime, 1000);
        }

        init();
    }
})();
