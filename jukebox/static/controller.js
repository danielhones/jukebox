var all_songs = [];
var filtered_songs = [];
var table_page = 0;
var ENTRIES_PER_PAGE = 100;
var current_song = {};


function load_next_song() {
    
}


function load_song(id) {
    current_song = all_songs[id];
    document.getElementById('audio-source').src = '/songs/' + id.toString() + '/file';
    document.getElementById('player').load();
    $('#currently_playing').html(current_song.artist_name + ' - ' + current_song.title);
    document.getElementById('player').onended = load_next_song;
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
        load_song($(this).data('song-id'),
                  $(this).data('song-title'),
                  $(this).data('song-artist'));
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
                append($('<td/>', {text: i.title})).
                append($('<td/>', {text: i.formatted_length})).
                append($('<td/>', {text: i.artist_name})).
                append($('<td/>', {text: i.album_title}))
        );
    });

    $('a.previous_page, a.first_page, a.next_page, a.last_page').removeClass('disabled');
    if (table_page == 0) {
        $('a.previous_page, a.first_page').addClass('disabled');
    }
    if (table_page == max_page()) {
        $('a.next_page, a.last_page').addClass('disabled');
    }
    var page_text = (table_page+1).toString() + " of " + (max_page()+1).toString();
    $('span.page_indicator').text(page_text);
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
