const inputText=document.getElementById("input-text");
const listContainer=document.getElementById("list-container");


function addTask() {

     if(inputText.value===''){
 
        alert("You must write something");
     }else{

          let li=document.createElement("li");
           li.innerHTML=inputText.value;
           listContainer.appendChild(li);
            
         let span=document.createElement('span')
             
             span.innerHTML='\u00d7';
             li.appendChild(span);
     }
        inputText.value='';

     

}
