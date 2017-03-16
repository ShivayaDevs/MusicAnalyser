
var filename = $('#filename-para').html();
console.log(filename);

/* Sending 3 requests serially, a parallel implementation would be better */

// Because genre comes fastest
get_genre();

function get_genre(){
    //
    $.ajax({
       url: '../ajax/genre/',
       data: {
           'filename': filename
       },
       dataType: 'json',
       success: setGenre
    });
}
function setGenre(data){
    console.log(data);
    var genre = data['genre'];
    genre = genre.charAt(0).toUpperCase() + genre.substring(1).toLowerCase();
    $('#genre-tv').html(genre + '!');
    console.log(genre + 'now fetching features');
    get_features();
}

function get_features(){
    $.ajax({
        url: '../ajax/features/',
        data: {
            'filename': filename
        },
        dataType: 'json',
        success: setFeatures
    });
}

/* SAMPLE DATA
centroid:39.13698433079813
centroid-image-url:"/static/images/spectral_centroid.png"
flux:6155.125163435292
flux-image-url:"/static/images/spectral_flux.png"
fourier-image-url:"/static/images/fourier.png"
number_samples:1323000
rms:6155.125163435292
rms-image-url:"/static/images/rms.png"
roll:6155.125163435292
roll-image-url:"/static/images/spectral_rolloff.png"
sample_rate:44100
wav-image-url:"/static/images/wavedata.png"
zero-crossing:0.059678805501742635
*/
function setFeatures(data){
    console.log(data);
    console.log('getting emotions');
    get_emotion();

    $('#main-animation').hide("slow", function(){});

    $('#sample-rate').html(data['sample_rate']);
    $('#number-samples').html(data['number_samples']);

    $('#wave-image').attr('src', data['wav-image-url']);
    $('#fourier-image').attr('src', data['fourier-image-url']);
    
    $('#zero-crossing').html('Zero Crossing Rate: ' + data['zero-crossing']);
    
    $('#rms').html('Root Mean Square(RMS): ' + data['rms']);
    $('#rms-image').attr('src', data['rms-image-url']);
    
    $('#spectral-centroid').html('Spectral Centroid: ' + data['centroid']);
    $('#centroid-image').attr('src', data['centroid-image-url']);
    
    $('#spectral-flux').html('Spectral Flux: ' + data['flux']);
    $('#flux-image').attr('src', data['flux-image-url']);    

    $('#spectral-rolloff').html('Spectral Roll: ' + data['roll']);
    $('#rolloff-image').attr('src', data['roll-image-url']);
}


/* Send a request to fetch emotion data */
$('#emo-div').hide();

function get_emotion(){
    $.ajax({
       url: '../ajax/emotion/',
       data: {
           'filename': filename
       },
       dataType: 'json',
       success: setEmotion
    });
}

function setEmotion(data){

    $('#small-animation').hide();
    $('#emo-div').show("slow",function(){});
    var emotion = data['emotion'];

    $('#emo-image').attr('src', data['emo_image_url']);
    emotion = emotion.charAt(0).toUpperCase() + emotion.substring(1).toLowerCase();
    $('#emo-name-display').html(emotion + '!');
    console.log(data);
}
