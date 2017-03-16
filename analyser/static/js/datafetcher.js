
var filename = $('#filename-para').html();
console.log(filename);

/* Sending 4 requests parallely */

/*******************************************************************/

/* Send a request to fetch emotion data */
//$.ajax({
//    url: '../ajax/emotion/',
//    data: {
//        'filename': filename
//    },
//    dataType: 'json',
//    success: setEmotion
//});

function setEmotion(data){
    $('#emo-name-display').html(data['emotion']);
    $('#emo-image').attr('src', data['emo_image_url']);
    console.log(data);
}

/*******************************************************************/
//
//$.ajax({
//    url: '../ajax/genre/',
//    data: {
//        'filename': filename
//    },
//    dataType: 'json',
//    success: setGenre
//});

function setGenre(data){
    console.log(data);
    $('#genre-tv').html(data['genre']);
}
/*******************************************************************/

$.ajax({
    url: '../ajax/features/',
    data: {
        'filename': filename
    },
    dataType: 'json',
    success: setFeatures
});
function setFeatures(data){
    console.log(data);
}


