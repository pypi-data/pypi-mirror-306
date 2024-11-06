///////////////////////////////////////////////////// 
/// utility functions
function getNumber(str) {
    // Regular expression to match the final digits
    let regex = /(\d+)$/;
    // Apply the regex to extract the digits at the end of the string
    let match = str.match(regex);
    // If a match is found, return the number, otherwise return null
    return match ? match[0] : null;
};

/// Global variables
const animations = Array.from(document.querySelectorAll('.animation'));
let animation_state = new Array(animations.length).fill(false);
let animation_on_stage = null;
let index0;
let position;

/////////////////////////////////////////////////////
//// Observer
const options = {
root: null, // Use the viewport as the root
rootMargin: '0px',
threshold: 0 // Trigger when the element is visible
};

const callback = (entries, observer) => {
entries.forEach((entry) => {
    let index = animations.findIndex(item => item.id === entry.target.id);
    if (entry.isIntersecting) {
            // new animation
            index0 = animation_state.findIndex(item => item === true);
            if (index0 == -1){
                    // set new
                    animation_on_stage = animations[index];
                    animation_on_stage.classList.remove('off_stage');
                    animation_on_stage.classList.add('on_stage');
                    console.log(animation_on_stage.id);
            }
            else{
                    if(index0 > index){
                            // remove old
                            animation_on_stage = null;
                            animations[index0].classList.remove('on_stage');
                            animations[index0].classList.add('off_stage');
                            // set new
                            animation_on_stage = animations[index];
                            animation_on_stage.classList.remove('off_stage');
                            animation_on_stage.classList.add('on_stage');
                    }
            };
            animation_state[index]=true;
    } 
    else {
            // bye animation
            index0 = animation_state.findIndex(item => item === true);
            if(index0 == -1  && animation_on_stage != null){
                    // remove inconsistency
                    animation_on_stage.classList.remove('on_stage');
                    animation_on_stage.classList.add('off_stage');
                    animation_on_stage = null;
            }
            else{
                    animation_state[index]=false;
                    if(index0 == index){
                            // remove
                            animation_on_stage = null;
                            animations[index].classList.remove('on_stage');
                            animations[index].classList.add('off_stage');
                            // set new
                            index0 = animation_state.findIndex(item => item === true);
                            if (index0 != -1){
                                    animation_on_stage = animations[index0];
                                    animation_on_stage.classList.remove('off_stage');
                                    animation_on_stage.classList.add('on_stage');
                                    console.log(animation_on_stage.id);
                            }
                    }
            };
    }
});
//console.log(animation_state);
//console.log(animation_on_stage)
};

const observer = new IntersectionObserver(callback, options);

// Observe each animation element
document.querySelectorAll('.animation').forEach(anima => {
observer.observe(anima);
});

/////////////////////////////////////////////////////        
//// Scroll    
// init scrolls
document.querySelectorAll('.animation').forEach(anima => {
const rect = anima.getBoundingClientRect();
id = getNumber(anima.id);
height = (-rect.top+rect.bottom) / window.innerHeight ;
document.body.style.setProperty('--scroll_'+id, 0);
document.body.style.setProperty('--height_'+id, height);
console.log('id','height:',height)
});
// scroll value
const setScroll = () => {
const rect = animation_on_stage.getBoundingClientRect();

position = (-rect.top+window.innerHeight)/(+rect.bottom-rect.top+window.innerHeight)*100;
//console.log('--> ',-rect.bottom+rect.top);
if (position<0){ position = 0;}
if (position>100){ position = 100;}

console.log(animation_on_stage.id+'>>> '+position);
id = getNumber(animation_on_stage.id);
document.body.style.setProperty('--scroll_'+id, position);
};
// listener         
window.addEventListener('scroll', () => {
//console.log(window.pageYOffset / (document.body.offsetHeight - window.innerHeight));
if (animation_on_stage != null){
    setScroll();
}
}, false);
