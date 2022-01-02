
const createSummary = document.getElementById("summary-form");
createSummary.onsubmit = 
function(e){
    e.preventDefault();
    chrome.tabs.getSelected(null, function(tab) {
        myFunction(tab.url);
    });
    
    function myFunction(tablink) {
      // do stuff here
      var video_id = tablink.split("?v=")[1].substr(0,11);
      // window.open("http://localhost:5000/trans?v="+video_id);
      window.open("https://yt-summerizer.herokuapp.com/trans?v="+video_id, '_blank');
      console.log(video_id)
    }
}


  

