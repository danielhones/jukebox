var all_songs = [];
var filtered_songs = [];
var table_page = 0;
var ENTRIES_PER_PAGE = 100;
var LOOP_QUEUE = false;
var current_song = {};
var current_queue = [];
var current_queue_index = 0;


function load_next_song() {
    current_queue_index += 1;
    if (current_queue_index == current_queue.length) {
        console.log("Reached end of queue.");
        return;
    }
    load_song(current_queue[current_queue_index].id, true);
}


function load_song(id, play) {
    current_song = all_songs[id];
    $('tr.song_row').removeClass('playing');
    $('tr.song_row[data-song-id=' + id + ']').addClass('playing');
    document.getElementById('audio-source').src = '/songs/' + id.toString() + '/file';
    document.getElementById('player').load();
    if (play) {
        document.getElementById('player').play();
    }
    $('#currently_playing').html(current_song.artist_name + ' - ' + current_song.title);
    document.getElementById('player').onended = load_next_song;
}


function update_queue(song_id) {
    var song = all_songs[song_id];
    var index = filtered_songs.indexOf(song);
    current_queue = filtered_songs.slice(index, filtered_songs.length);
    current_queue_index = 0;
}


function max_page() {
    return Math.floor(filtered_songs.length / ENTRIES_PER_PAGE);
}


function first_page() {
    table_page = 0;
    update_table();
}


function last_page() {
    table_page = max_page();
    update_table();
}


function previous_page() {
    table_page += -1;
    if (table_page < 0) {
        table_page = 0;
    }
    update_table();
}


function next_page() {
    table_page += 1;
    if (table_page > max_page()) {
        table_page = max_page();
    }
    update_table();
}


function clickable_song_row() {
    $('tr.song_row').on('click', function() {
        var song_id = $(this).data('song-id');
        update_queue(song_id);
        load_song(song_id);
    });
    $('tr.song_row').on('dblclick', function() {
        var song_id = $(this).data('song-id');
        update_queue(song_id);
        load_song(song_id, true);
    });
}

function update_table() {
    var start = table_page * ENTRIES_PER_PAGE;
    var items = filtered_songs.slice(start, start + ENTRIES_PER_PAGE - 1);
    $('tbody tr').remove();

    items.forEach(function(i) {
        $('tbody').append(
            $('<tr/>', {class: 'song_row',
                        'data-song-id': i.id,
                        'data-song-title': i.title,
                        'data-song-artist': i.artist_name
                       }).
                append($('<td/>', {text: i.title, class: 'song_title'})).
                append($('<td/>', {text: i.formatted_length})).
                append($('<td/>', {text: i.artist_name})).
                append($('<td/>', {text: i.album_title}))
        );
    });

    $('tr[data-song-id=' + current_song.id + ']').addClass('playing');
    $('a.previous_page, a.first_page, a.next_page, a.last_page').removeClass('disabled');
    if (table_page == 0) {
        $('a.previous_page, a.first_page').addClass('disabled');
    }
    if (table_page == max_page()) {
        $('a.next_page, a.last_page').addClass('disabled');
    }
    var page_text = (table_page+1).toString() + " of " + (max_page()+1).toString();
    $('span.page_indicator').text(page_text);
    $('#result_count').text(filtered_songs.length.toString() + ' songs');
    clickable_song_row();
}


function filter_songs() {
    var words = $('#filter_input').val().split(/\s+/);
    filtered_songs = [];
    Object.keys(all_songs).forEach( function(i) {
        var song = all_songs[i];
        var check = song.title.toLowerCase() + song.artist_name.toLowerCase() + song.album_title.toLowerCase();
        var match = words.every(function(word) {
            return (check.indexOf(word.toLowerCase()) != -1);
        });
        if (match) {
            filtered_songs.push(song);
        }
    });
    table_page = 0;
    update_table();
}


function set_player_css() {
    var playerViewPadding = parseInt($('#player-view').css('padding-top'), 10);
    var playerHeight = $('#player').outerHeight();
    var playerViewHeight = playerHeight + playerViewPadding * 2;
    if ($('#currently_playing').width() / $('#player-view').width() > 0.6) {
        playerViewHeight += 24;
    }
    $('#player-view').css('height', playerViewHeight);
    $('#manager-view').css('height', window.innerHeight - playerViewHeight);
}


$(document).ready(function() {
    set_player_css();
    $(window).on('resize', set_player_css);
    clickable_song_row();

    $('a.next_page').on('click', next_page);
    $('a.previous_page').on('click', previous_page);
    $('a.first_page').on('click', first_page);
    $('a.last_page').on('click', last_page);

    $.ajax({
        url: '/songs.json',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            all_songs = data;
            filtered_songs = [];
            Object.keys(all_songs).forEach( function(i) {
                filtered_songs.push(all_songs[i]);
            });
            update_table();
            $('#filter_input').on('input', function() { filter_songs(); });
        }
    });    
});
