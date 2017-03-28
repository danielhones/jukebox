function load_song(id) {
    console.log("Loading song", id);
    document.getElementById('audio-source').src = '/song/' + id.toString();
    //document.getElementById('audio-source').src = '/song/' + id.toString();
    document.getElementById('player').load();
}


function set_player_css() {
    var playerViewPadding = parseInt($('#player-view').css('padding-top'), 10);
    var playerHeight = $('#player').outerHeight();
    var playerViewHeight = playerHeight + playerViewPadding * 2;
    $('#player-view').css('height', playerViewHeight);
    $('#manager-view').css('height', window.innerHeight - playerViewHeight);
}


$(document).ready(function() {
    set_player_css();
    $(window).on('resize', set_player_css);
    $('td.song_row').on('click', function() {
        load_song($(this).data('song-id'));
    });
});
