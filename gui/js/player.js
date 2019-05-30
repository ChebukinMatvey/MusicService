var played_block 


function play_click(img_block) {
    track_index = parseInt(img_block.parentElement.children[0].innerHTML) - 1
    start_play(track_index)
}

function start_play(index) {
    el = track_list[index]
    if(played_block != undefined)
        played_block.removeClass('current-play')
    played_block = $($("#list li")[index])
    played_block.addClass('current-play')
    if (player != undefined) {
        player.stop()
        delete player
    }
    $.ajax({
        method: 'GET',
        async: false,
        url: `https://zvuk.com/api/tiny/track/stream?id=${el.stream}&quality=high`,
    }).done(resp => {
        player = new Howl({
            src: [resp.result.stream],
            format: ['mp3', 'aac'],
            html5: true,
            volume:current_volume
        })
        player.on('play', on_player_play)
        player.on('load', on_player_load)
        player.on('end', next)
        setInterval(audioState,1000)
    })
}

function on_player_load() {
    $("div.player").show()
    player.play()
}

function on_player_play() {
    console.log("Playing...")
    track = track_list[track_index]
    $($("img#player-image")[0]).attr('src', track.img)
    $($('div.player-name-and-artist > p.track-name')[0]).html(track.name)
    $($('div.player-name-and-artist > p.track-artists')[0]).html(track.artists[0])
    $($("i.play")[0]).hide()
    $($("i.pause")[0]).show()
}


function play() {
    player.play()
    $($("i.pause")[0]).hide()
    $($("i.play")[0]).show()
}

function pause() {
    player.pause()
    $($("i.play")[0]).show()
    $($("i.pause")[0]).hide()
}

function next() {
    if (track_index + 1 < track_list.length)
        start_play(++track_index)
    else
        console.log("No track forward")
}


function seekAudio(value){
    duration = player.duration()    
    position = (parseInt(value)/100)*duration
    player.seek(position)
}

function previous() {
    if (track_index - 1 >= 0)
        start_play(--track_index)
    else
        console.log("No track behind")
}

function setVolume(value) {
    current_volume = parseInt(value)/100
    player.volume(current_volume)
}

function audioState(){
    let duration = player.duration()
    let val = (parseInt((player.seek()/duration)*100))
    $($("input#audio-state")[0]).val(val)
}