
var filename = $('#filename-para').html();
console.log(filename);

/* Sending 4 requests parallely */

/*******************************************************************/

/* Send a request to fetch emotion data */
$.ajax({
    url: '../ajax/emotion/',
    data: {
        'filename': filename
    },
    dataType: 'json',
    success: setEmotion
});

function setEmotion(data){
    $('#emo-name-display').html(data['emotion']);
    $('#emo-image').attr('src', data['emo_image_url']);
    console.log(data);
}

/*******************************************************************/
$.ajax({
    url: '../ajax/tags/',
    data: {
        'filename': filename
    },
    dataType: 'json',
    success: setTags
});
/*******************************************************************/

$.ajax({
    url: '../ajax/genre/',
    data: {
        'filename': filename
    },
    dataType: 'json',
    success: setGenre
});
/*******************************************************************/

$.ajax({
    url: '../ajax/features/',
    data: {
        'filename': filename
    },
    dataType: 'json',
    success: setFeatures
});

