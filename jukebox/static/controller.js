$(function() {
    var playerViewPadding = parseInt($('#player-view').css('padding-top'), 10);
    var playerHeight = $('#player').outerHeight();
    var playerViewHeight = playerHeight + playerViewPadding * 2;
    $('#player-view').css('height', playerViewHeight);
    $('#manager-view').css('height', window.innerHeight - playerViewHeight);

    // Load sample audio file:
    document.getElementById('audio-source').src = '/static/untitled.mp3';
    document.getElementById('player').load();
});
