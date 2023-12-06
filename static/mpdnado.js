window.onload = () => {
  document.getElementById("volume").addEventListener("change", volumeChange);
  document.getElementById("play").addEventListener("click", togglePlay);
  window.setInterval(queryCurrSong, 2000);
}

/**-----------------------------------------------------------------------
 * Perform an XMLHTTPRequest (XHR). Command and value (optional) are passed
 * as URL parameters, `{xhr_url}?command=value`. If a callback function is
 * provided, it is called (async) and passed the raw XHR response.
 *
 * @param {string} command - The command to send.
 * @param {string} value - The value to send. (opt)
 * @param {function} callback - Function called to handle response. (opt)
-----------------------------------------------------------------------*/
function xhr(command, value=null, callback=null) {
  var xmlreq = new XMLHttpRequest();

  if (callback) {
    xmlreq.onreadystatechange = () => {
      if (xmlreq.readyState === 4) {
        callback(xmlreq.response)
      }
    }
  }

  URL = "http://" + location.host + "/xhr?" + command;
  if (value) {
    URL += "=" + value
  }
  console.log("XHR: " + URL);
  xmlreq.open("GET", URL);
  xmlreq.send();
}

/**-----------------------------------------------------------------------
 * Query current song title via XHR.
 -----------------------------------------------------------------------*/
function queryCurrSong() {
  xhr("song", null, updateCurrSong)
}

/**-----------------------------------------------------------------------
 * Update the `currentsong` element text to the provided `title`.
 *
 * @param {string} title - The title of the song.
 -----------------------------------------------------------------------*/
function updateCurrSong(json) {
  console.log(json)
  songInfo = JSON.parse(json);
  document.getElementById("song_name").textContent = songInfo.name;
  document.getElementById("song_title").textContent = songInfo.title;
}

/**-----------------------------------------------------------------------
 * Change volume based on `volume` slider element. The current slider
 * position is read and sent via XHR.
 -----------------------------------------------------------------------*/
function volumeChange() {
  volume = document.getElementById("volume").value;
  console.log("VOLUME: " + volume);
  xhr("volume", volume);
}

/**-----------------------------------------------------------------------
 * Send a play toggle request via XHR.
 -----------------------------------------------------------------------*/
function togglePlay() {
  console.log("PLAY");
  xhr("play");
}