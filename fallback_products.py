<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Prodpick4U Full Multi-User Wall with TTS</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap">
<style>
body{font-family:'Inter',sans-serif;margin:0;padding:1rem;color:#fff;background: linear-gradient(-45deg,#0a0033,#3b007f,#1a1aff,#6f00ff);background-size:400% 400%;animation: gradientShift 15s ease infinite;}
@keyframes gradientShift{0%{background-position:0% 50%;}25%{background-position:50% 50%;}50%{background-position:100% 50%;}75%{background-position:50% 50%;}100%{background-position:0% 50%;}}
h1,h2,h3,h4{color:#9cf;}
h1{text-align:center;font-size:2rem;margin-bottom:1rem;}
p{line-height:1.4;}
.glass{background: rgba(0,0,0,0.5);backdrop-filter: blur(10px);border-radius:12px;padding:15px;margin-bottom:1rem;}
input, button, select{width:100%;padding:10px;margin:5px 0;border-radius:5px;border:none;}
input, select{background: rgba(20,20,20,0.7); color:#fff;}
button{background: linear-gradient(135deg,#6a11cb,#2575fc); color:#fff; font-weight:bold; cursor:pointer;}
button:hover{opacity:0.85;}
.output{background:rgba(0,0,0,0.7);padding:10px;border-radius:8px;margin-top:8px;color:#0f0;white-space:pre-wrap;}
.section-title{font-size:1.3rem;margin-bottom:0.8rem;text-align:center;}
.timer{text-align:center;font-size:0.9rem;margin-bottom:0.8rem;color:#ff0;}
.collapsible{background-color: rgba(0,0,0,0.5); color:#fff; cursor:pointer; padding: 10px; width:100%; border:none; text-align:left; font-size:1rem; border-radius:6px; margin-bottom:5px;}
.collapsible.active{background-color: rgba(75,0,150,0.7);}
.content{padding:10px 5px; max-height:0; overflow:hidden; transition:max-height 0.3s ease; background-color: rgba(0,0,0,0.3); border-radius:6px; margin-bottom:8px;}
.product-wall{display:flex; flex-wrap:wrap; gap:10px; justify-content:center;}
.product-card{background: rgba(20,20,20,0.6); padding:8px; border-radius:6px; width:45%; text-align:center;}
.product-card img{max-width:100%; border-radius:6px; margin-bottom:5px;}
a{color:#9cf; text-decoration:none;}
a:hover{text-decoration:underline;}
@media(min-width:600px){.product-card{width:200px;}}
.teleprompter{background: rgba(0,0,0,0.6); padding:10px; border-radius:6px; margin-top:10px;}
</style>
</head>
<body>

<h1>🚀 Prodpick4U Multi-User Wall with TTS</h1>

<div class="glass">
<h2 class="section-title">🔒 Affiliate Access</h2>
<p>Enter your access code:</p>
<input type="text" id="accessCode" placeholder="Enter your code">
<button onclick="checkAccessCode()">Unlock Wall</button>
<div id="accessOutput" class="output"></div>
</div>

<div id="affiliateFormSection" class="glass" style="display:none;">
<h2 class="section-title">📝 Register Your Affiliate Tag</h2>
<form id="affiliateForm">
<label>Your Amazon Affiliate Tag:
  <input type="text" id="userAffiliate" placeholder="mytag-20" required>
</label>
<button type="submit">Activate</button>
</form>
<div id="regOutput" class="output"></div>
<div id="demoTimer" class="timer"></div>
</div>

<div id="productWall" class="glass"></div>

<div class="glass teleprompter">
<h2 class="section-title">🖋️ Teleprompter / TTS</h2>
<textarea id="teleprompterText" rows="4" placeholder="Click a product to load 60-second script..." style="width:100%;background:rgba(20,20,20,0.7);color:#fff;border-radius:6px;padding:8px;"></textarea>
<button onclick="playTTS()">🔊 Play TTS</button>
</div>

<script>
// ===== Multi-User Access Codes =====
const VALID_CODES = ["starter123","user456","demo789"];
let userAffiliateTag = localStorage.getItem('affiliateTag') || "";

// ===== Full Fallback Products with Thumbnails =====
const FALLBACK_PRODUCTS = {
"health":[
{title:"Fitbit Charge 5", url:"https://amzn.to/45zc4k1", price:"$129.95", image:"https://m.media-amazon.com/images/I/71smqRr0pmL._AC_SL1500_.jpg", description:"Fitness tracker with built-in GPS and health metrics."},
{title:"Theragun Elite", url:"https://amzn.to/463BPYL", price:"$299.00", image:"https://m.media-amazon.com/images/I/71U3g1V+lFL._AC_SL1500_.jpg", description:"Professional-grade percussive therapy device for deep muscle treatment and recovery."},
{title:"Methylene Blue", url:"https://amzn.to/4ldkJwL", price:"Varies", image:"https://m.media-amazon.com/images/I/61bNfb0TcaL._AC_SL1500_.jpg", description:"Supplement for mitochondrial support and cognitive function."},
{title:"Irish Sea Moss", url:"https://www.amazon.com/dp/B0CTMJYZ73?tag=mychanneld-20", price:"Varies", image:"https://m.media-amazon.com/images/I/71pKQev7ZSL._AC_SL1500_.jpg", description:"Rich in iodine and essential minerals for immune and thyroid support."},
{title:"Shilajit", url:"https://amzn.to/4li6vuC", price:"Varies", image:"https://m.media-amazon.com/images/I/61MPYz5RXnL._AC_SL1500_.jpg", description:"Ancient herbal resin used to boost energy, vitality, and performance."}
],
"beauty":[
{title:"Revlon One-Step Hair Dryer", url:"https://amzn.to/3HIHhrw", price:"$59.99", image:"https://m.media-amazon.com/images/I/71tG1vTk4sL._AC_SL1500_.jpg", description:"Hair styling tool for drying and volumizing."},
{title:"Olay Regenerist Cream", url:"https://amzn.to/45zc4k1", price:"$25.99", image:"https://m.media-amazon.com/images/I/71xJSt9W77L._AC_SL1500_.jpg", description:"Anti-aging facial moisturizer."},
{title:"Neutrogena Makeup Remover", url:"https://amzn.to/3UAEOSX", price:"$9.99", image:"https://m.media-amazon.com/images/I/81vZqCldg0L._AC_SL1500_.jpg", description:"Gentle wipes for makeup removal."},
{title:"Maybelline Lash Sensational Mascara", url:"https://amzn.to/4oHMpgn", price:"$7.99", image:"https://m.media-amazon.com/images/I/61P5o4xqopL._AC_SL1500_.jpg", description:"Volumizing mascara with buildable formula."},
{title:"CeraVe Hydrating Cleanser", url:"https://amzn.to/4mI68uu", price:"$14.99", image:"https://m.media-amazon.com/images/I/81Xy4oV+mGL._AC_SL1500_.jpg", description:"Gentle face cleanser for normal to dry skin."}
],
"kitchen":[
{title:"Instant Pot Duo 7-in-1", url:"https://amzn.to/4oD8b50", price:"$89.00", image:"https://m.media-amazon.com/images/I/81kL7YtP+1L._AC_SL1500_.jpg", description:"Multi-functional pressure cooker."},
{title:"Lodge Cast Iron Skillet", url:"https://amzn.to/47igIUx", price:"$24.99", image:"https://m.media-amazon.com/images/I/91j4X2UKjEL._AC_SL1500_.jpg", description:"Durable pre-seasoned cast iron pan."},
{title:"Breville Smart Oven Air Fryer", url:"https://amzn.to/45lPvxL", price:"$279.95", image:"https://m.media-amazon.com/images/I/71K3cXx5zJL._AC_SL1500_.jpg", description:"Countertop convection oven with air fryer."},
{title:"KitchenAid Artisan Stand Mixer", url:"https://amzn.to/45lPCJH", price:"$379.99", image:"https://m.media-amazon.com/images/I/81CJbOlb2SL._AC_SL1500_.jpg", description:"Versatile stand mixer for baking."},
{title:"Cuisinart 14-Cup Food Processor", url:"https://amzn.to/3UgiUEs", price:"$149.95", image:"https://m.media-amazon.com/images/I/81X6+GxzTRL._AC_SL1500_.jpg", description:"Powerful food processor for chopping and slicing."},
{title:"Ninja Foodi 9-in-1", url:"https://amzn.to/3H8Olh3", price:"$199.99", image:"https://m.media-amazon.com/images/I/71FhZJx0nYL._AC_SL1500_.jpg", description:"Multi-cooker with air frying and pressure cooking features."},
{title:"NutriBullet Pro", url:"https://amzn.to/47eVzKT", price:"$89.99", image:"https://m.media-amazon.com/images/I/81eObhW9DML._AC_SL1500_.jpg", description:"Compact blender for smoothies and shakes."},
{title:"Hydro Flask Water Bottle", url:"https://amzn.to/4myBCTZ", price:"$39.95", image:"https://m.media-amazon.com/images/I/71aI7y1Hu6L._AC_SL1500_.jpg", description:"Vacuum insulated bottle keeps drinks cold or hot."}
],
"tech":[
{title:"Apple AirPods Pro", url:"https://amzn.to/3UAYMx7", price:"$249.00", image:"https://m.media-amazon.com/images/I/71zny7BTRlL._AC_SL1500_.jpg", description:"Premium ANC, deep spatial audio, Apple ecosystem."},
{title:"Samsung Galaxy Buds FE", url:"https://amzn.to/4m6BhIh", price:"$99.99", image:"https://m.media-amazon.com/images/I/61MqQKD9hXL._AC_SL1500_.jpg", description:"Reliable ANC earbuds for Android users."},
{title:"Anker Soundcore P20i", url:"https://amzn.to/4mqytoV", price:"$29.99", image:"https://m.media-amazon.com/images/I/61kLdvG0MQL._AC_SL1500_.jpg", description:"Budget wireless earbuds."},
{title:"Samsung T7 Portable SSD", url:"https://amzn.to/3J1xAor", price:"$139.99", image:"https://m.media-amazon.com/images/I/71aAY2vnpnL._AC_SL1500_.jpg", description:"Fast external solid state drive."},
{title:"Logitech MX Master 3S Mouse", url:"https://amzn.to/4oFWA4T", price:"$99.99", image:"https://m.media-amazon.com/images/I/61iFV+PYObL._AC_SL1500_.jpg", description:"Ergonomic wireless mouse with high-precision tracking."},
{title:"Sony WH-1000XM4 Headphones", url:"https://amzn.to/3V5ToC2", price:"$199.99", image:"https://m.media-amazon.com/images/I/71o8Q5XJS5L._AC_SL1500_.jpg", description:"Noise-canceling headphones with long battery life."},
{title:"Kindle Paperwhite 2024", url:"https://amzn.to/4mTKZOd", price:"$159.99", image:"https://m.media-amazon.com/images/I/61QFuhZ8O6L._AC_SL1500_.jpg", description:"Waterproof e-reader with 7-inch display."}
],
"outdoors":[
{title:"Coleman Sundome Tent", url:"https://amzn.to/4myC9oX", price:"$99.99", image:"https://m.media-amazon.com/images/I/81Gzm4fDb3L._AC_SL1500_.jpg", description:"Easy setup tent for camping."},
{title:"LifeStraw Personal Water Filter", url:"https://amzn.to/4m3CoIw", price:"$19.97", image:"https://m.media-amazon.com/images/I/71lC7iT77JL._AC_SL1500_.jpg", description:"Portable water purifier for outdoor use."},
{title:"Etekcity Lantern", url:"https://amzn.to/41tkYwL", price:"$23.99", image:"https://m.media-amazon.com/images/I/71jcFblG0AL._AC_SL1500_.jpg", description:"LED camping lantern with adjustable brightness."},
{title:"Osprey Atmos AG Backpack", url:"https://amzn.to/40RUG7h", price:"$260.00", image:"https://m.media-amazon.com/images/I/81mC+txG6dL._AC_SL1500_.jpg", description:"Comfortable hiking backpack with ventilation."},
{title:"Garmin GPSMAP Handheld GPS", url:"https://amzn.to/45BCoJX", price:"$399.99", image:"https://m.media-amazon.com/images/I/71YsQ7P4I1L._AC_SL1500_.jpg", description:"Rugged GPS device for outdoor navigation."}
],
"household":[
{title:"iRobot Roomba 694", url:"https://amzn.to/4flpTp8", price:"$249.99", image:"https://m.media-amazon.com/images/I/71Xgtd3nQNL._AC_SL1500_.jpg", description:"Smart robot vacuum for home cleaning."},
{title:"Dyson V8 Absolute", url:"https://amzn.to/4fll1QY", price:"$399.99", image:"https://m.media-amazon.com/images/I/71f4NErPzvL._AC_SL1500_.jpg", description:"Powerful cordless vacuum cleaner."},
{title:"Instant Pot Duo Crisp", url:"https://amzn.to/3J1ZhxC", price:"$159.99", image:"https://m.media-amazon.com/images/I/81nHpq2DbWL._AC_SL1500_.jpg", description:"Multi-use pressure cooker with air fryer lid."},
{title:"Philips Hue Smart Bulb", url:"https://amzn.to/4fxUPCY", price:"$49.99", image:"https://m.media-amazon.com/images/I/61t87MAL-IL._AC_SL1500_.jpg", description:"Smart LED bulb with app control."},
{title:"Nespresso Vertuo Coffee Maker", url:"https://amzn.to/46LByvu", price:"$199.00", image:"https://m.media-amazon.com/images/I/71QeA5HcLJL._AC_SL1500_.jpg", description:"Single serve coffee and espresso machine."}
],
"home-decor":[
{title:"Amethyst Feng Shui Tree", url:"https://www.amazon.com/dp/B0B8QWN9NT?tag=mychanneld-20", price:"$39.95", image:"https://m.media-amazon.com/images/I/71XK9E3bKDL._AC_SL1500_.jpg", description:"Handcrafted amethyst crystal tree symbolizing peace."},
{title:"Linon Brooklyn Sherpa Chair", url:"https://www.amazon.com/dp/B083TRV28M?tag=mychanneld-20", price:"$129.99", image:"https://m.media-amazon.com/images/I/71Qj0Pe9cSL._AC_SL1500_.jpg", description:"Ivory sherpa office chair with adjustable height."},
{title:"Jersey Wall Waterfall XL", url:"https://www.amazon.com/dp/B01KP0ONSY?tag=mychanneld-20", price:"$399.99", image:"https://m.media-amazon.com/images/I/71xUj6HpkzL._AC_SL1500_.jpg", description:"Large wall-mounted waterfall for tranquil ambiance."},
{title:"Medify MA-40 Air Purifier", url:"https://www.amazon.com/dp/B07LGDYV3C?tag=mychanneld-20", price:"$249.99", image:"https://m.media-amazon.com/images/I/71q+hlxG3XL._AC_SL1500_.jpg", description:"Covers up to 1,793 sq ft with HEPA H13 filter."},
{title:"Relaxing Liquid Motion Lamp", url:"https://www.amazon.com/dp/B0DRBZS1DR?tag=mychanneld-20", price:"$44.95", image:"https
:"https://m.media-amazon.com/images/I/61e5vVZyzFL._AC_SL1500_.jpg", description:"Soothing liquid motion lamp with vibrant colors for relaxation."},
{title:"VIAHART 14\" Glass Mini Aquarium", url:"https://www.amazon.com/dp/B0CRDP8TM9?tag=mychanneld-20", price:"$69.99", image:"https://m.media-amazon.com/images/I/71r9yOeCz+L._AC_SL1500_.jpg", description:"Compact glass mini aquarium for tabletop decoration."}
]
};

// ===== Display Products =====
function renderProductWall() {
  const wall = document.getElementById("productWall");
  wall.innerHTML = "";
  Object.keys(FALLBACK_PRODUCTS).forEach(cat => {
    const collapsible = document.createElement("button");
    collapsible.className = "collapsible";
    collapsible.innerText = `📦 ${cat.toUpperCase()}`;
    collapsible.addEventListener("click", function(){
      this.classList.toggle("active");
      const content = this.nextElementSibling;
      if(content.style.maxHeight) {content.style.maxHeight=null;}
      else{content.style.maxHeight = content.scrollHeight + "px";}
    });
    wall.appendChild(collapsible);

    const contentDiv = document.createElement("div");
    contentDiv.className = "content product-wall";
    FALLBACK_PRODUCTS[cat].forEach(product => {
      const card = document.createElement("div");
      card.className = "product-card";
      card.innerHTML = `<img src="${product.image}" alt="${product.title}">
                        <h4>${product.title}</h4>
                        <p>${product.price}</p>
                        <p>${product.description}</p>
                        <a href="${product.url}" target="_blank">Buy Now</a>`;
      card.addEventListener("click", ()=> {
        document.getElementById("teleprompterText").value = generateTeleprompter(product);
      });
      contentDiv.appendChild(card);
    });
    wall.appendChild(contentDiv);
  });
}

// ===== Generate 60-second Teleprompter Script =====
function generateTeleprompter(product) {
  return `🎬 60-Second Teleprompter Script for "${product.title}":\n
Hello everyone! Today I want to introduce you to the amazing product "${product.title}". This product is perfect for those who want ${product.description.toLowerCase()}. Priced at ${product.price}, it offers excellent value. You can order it directly via this link: ${product.url}. Don't miss the chance to enhance your life with this incredible item. Thank you for watching and stay tuned for more top recommendations!`;
}

// ===== TTS =====
function playTTS() {
  const text = document.getElementById("teleprompterText").value;
  if(!text){alert("Please select a product to generate TTS."); return;}
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = "en-US";
  speechSynthesis.speak(utter);
}

// ===== Access Code Validation =====
function checkAccessCode() {
  const code = document.getElementById("accessCode").value;
  const output = document.getElementById("accessOutput");
  if(VALID_CODES.includes(code)){
    output.textContent = "✅ Access Granted!";
    document.getElementById("affiliateFormSection").style.display = "block";
    renderProductWall();
  } else {
    output.textContent = "❌ Invalid code.";
  }
}

// ===== Affiliate Form =====
document.getElementById("affiliateForm").addEventListener("submit", function(e){
  e.preventDefault();
  userAffiliateTag = document.getElementById("userAffiliate").value;
  localStorage.setItem("affiliateTag", userAffiliateTag);
  document.getElementById("regOutput").textContent = `Affiliate tag "${userAffiliateTag}" saved! Enjoy browsing.`;
});

// ===== Demo Timer Example =====
let demoSeconds = 300; // 5 minutes demo
function startDemoTimer() {
  const timerEl = document.getElementById("demoTimer");
  const interval = setInterval(() => {
    if(demoSeconds <= 0){clearInterval(interval); timerEl.textContent="⏰ Demo expired"; return;}
    let mins = Math.floor(demoSeconds/60);
    let secs = demoSeconds % 60;
    timerEl.textContent = `⏳ Demo time remaining: ${mins}m ${secs}s`;
    demoSeconds--;
  },1000);
}
startDemoTimer();

</script>

</body>
</html>
