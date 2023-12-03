window.onload = () => {
  document.getElementById("volume").addEventListener("change", volumeChange);
  document.getElementById("play").addEventListener("click", togglePlay);
  window.setInterval(queryCurrSong, 2000);
}

/**-----------------------------------------------------------------------
 * Perform an XMLHTTPRequest (XHR). Command and value (optiona) are passed
 * as URL parameters, `{xhr_url}?command=value`. If a callback function is
 * provided, it is called (async) and passed raw XHR response.
 *
 * @param {string} command - The command to send.
 * @param {string} value - Any parameters
 * @param {function} callback -
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

  if (value) {
    xmlreq.open("GET", "http://" + location.host + "/xhr?" + command + "=" + value);
  } else {
    xmlreq.open("GET", "http://" + location.host + "/xhr?" + command);
  }
  xmlreq.send();
}

/**-----------------------------------------------------------------------
 * Query current song title via XHR.
 -----------------------------------------------------------------------*/
function queryCurrSong() {
  xhr("song", "current", updateCurrSong)
}

/**-----------------------------------------------------------------------
 * Update the `currentsong` element text to the provided `title`.
 *
 * @param {string} title - The title of the song.
 -----------------------------------------------------------------------*/
function updateCurrSong(title) {
  console.log(title)
  document.getElementById("currentsong").textContent = title
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