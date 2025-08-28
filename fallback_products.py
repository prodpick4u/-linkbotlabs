<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Product Catalog</title>
<style>
body { font-family: Arial, sans-serif; background: #f4f4f9; color: #333; padding: 20px; }
h1 { text-align: center; }
select { padding: 10px; margin: 10px 0; width: 100%; max-width: 400px; }
.product-info { margin: 10px 0; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
.category-Health { background-color: #ffdddd; }
.category-Beauty { background-color: #ffe0f0; }
.category-Kitchen { background-color: #fff0cc; }
.category-Tech { background-color: #ddeeff; }
.category-Outdoors { background-color: #ddffdd; }
.category-Household { background-color: #f0f0f0; }
.category-HomeDecor { background-color: #e0e0ff; }
.more-info { margin-top: 10px; display: inline-block; padding: 5px 10px; background: #007bff; color: #fff; border-radius: 3px; cursor: pointer; }
</style>
<script src="https://js.puter.com/v2/"></script>
</head>
<body>

<h1>Product Catalog</h1>

<select id="categorySelect">
    <option value="">Select a category</option>
    <option value="Health">Health</option>
    <option value="Beauty">Beauty</option>
    <option value="Kitchen">Kitchen</option>
    <option value="Tech">Tech</option>
    <option value="Outdoors">Outdoors</option>
    <option value="Household">Household</option>
    <option value="HomeDecor">Home Decor</option>
</select>

<select id="productSelect" disabled>
    <option value="">Select a product</option>
</select>

<div id="productDetails"></div>

<script>
const AFFILIATE_TAG = "mychanneld-20";

function applyAffiliate(url){
    try {
        const ref = document.referrer;
        if(ref.includes("starter")) {
            if(url.includes("amazon.com/dp/") && !url.includes(`tag=${AFFILIATE_TAG}`)){
                return url.includes("?") ? `${url}&tag=${AFFILIATE_TAG}` : `${url}?tag=${AFFILIATE_TAG}`;
            }
        }
    } catch(e){}
    return url;
}

 Product Details -->
<div id="productDetails"></div>

<script>
// Combined products from temu_fallback.py + fallback_products.py
const AFFILIATE_TAG = "mychanneld-20";

// Temu products
const TEMU_PRODUCTS = [
    {title:"Multi Rice Cooker", url:"https://share.temu.com/jwZL6Tbh2SB", price:"Check Temu UK", description:"Versatile rice cooker for perfect meals", category:"Kitchen"},
    {title:"Foldable Kettle", url:"https://share.temu.com/GZe6nSeHcEB", price:"Check Temu UK", description:"Compact foldable kettle for quick boiling", category:"Kitchen"},
    {title:"Food Processor", url:"https://share.temu.com/xnKAVQF3V7B", price:"Check Temu UK", description:"Multifunctional food processor for your kitchen", category:"Kitchen"},
    {title:"Hot Air Oven", url:"https://share.temu.com/8O9QYZ5o0eB", price:"Check Temu UK", description:"Bake and roast easily with this hot air oven", category:"Kitchen"},
    {title:"Air Fryer", url:"https://share.temu.com/dQd6lwfzxcB", price:"Check Temu UK", description:"Healthy frying made easy with this air fryer", category:"Kitchen"},
    {title:"6-in-1 Cordless Vacuum Cleaner", url:"https://share.temu.com/7Qvf8xaoKiB", price:"Check Temu UK", description:"Lightweight cordless vacuum for quick cleaning", category:"Household"},
    {title:"Mortar and Pestle", url:"https://share.temu.com/DCHsUHCDe2B", price:"Check Temu UK", description:"Grind spices and herbs the traditional way", category:"Kitchen"},
    {title:"Ceiling Fan Light", url:"https://share.temu.com/Nops5j7hFnB", price:"Check Temu UK", description:"Modern ceiling fan with integrated light", category:"Household"},
    {title:"5L Cooker", url:"https://share.temu.com/sCWvXsTkDLB", price:"Check Temu UK", description:"Large 5L cooker for family meals", category:"Kitchen"}
];

// Fallback products
const FALLBACK_PRODUCTS = {
    Health: [
        {title:"Fitbit Charge 5 Advanced Fitness & Health Tracker", url:"https://amzn.to/45zc4k1", price:"$129.95", description:"Fitness tracker with built-in GPS and health metrics."},
        {title:"Theragun Elite Handheld Percussive Therapy Device", url:"https://amzn.to/463BPYL", price:"$299.00", description:"Professional-grade percussive therapy device for deep muscle treatment and recovery."},
        {title:"Methylene Blue", url:"https://amzn.to/4ldkJwL", price:"Varies", description:"Supplement researched for mitochondrial support and cognitive function."},
        {title:"Irish Sea Moss", url:`https://www.amazon.com/dp/B0CTMJYZ73?tag=${AFFILIATE_TAG}`, price:"Varies", description:"Rich in iodine and essential minerals for immune and thyroid support."},
        {title:"Shilajit", url:"https://amzn.to/4li6vuC", price:"Varies", description:"Ancient herbal resin used to boost energy, vitality, and performance."}
    ],
    Beauty: [
        {title:"Revlon One-Step Hair Dryer And Volumizer Hot Air Brush", url:"https://amzn.to/3HIHhrw", price:"$59.99", description:"Hair styling tool for drying and volumizing."},
        {title:"Olay Regenerist Micro-Sculpting Cream Face Moisturizer", url:"https://amzn.to/3HwMhQ8", price:"$25.99", description:"Anti-aging facial moisturizer."},
        {title:"Neutrogena Makeup Remover Cleansing Towelettes", url:"https://amzn.to/3UAEOSX", price:"$9.99", description:"Gentle wipes for makeup removal."},
        {title:"Maybelline Lash Sensational Washable Mascara", url:"https://amzn.to/4oHMpgn", price:"$7.99", description:"Volumizing mascara with buildable formula."},
        {title:"CeraVe Hydrating Facial Cleanser", url:"https://amzn.to/4mI68uu", price:"$14.99", description:"Gentle face cleanser for normal to dry skin."}
    ],
    Kitchen: [
        {title:"Instant Pot Duo 7-in-1 Electric Pressure Cooker", url:"https://amzn.to/4oLDhqU", price:"$89.00", description:"Multi-functional pressure cooker."},
        {title:"Lodge Cast Iron Skillet", url:"https://amzn.to/4oKl7WG", price:"$24.99", description:"Durable pre-seasoned cast iron pan."},
        {title:"Breville The Smart Oven Air Fryer", url:"https://amzn.to/47BJoYI", price:"$279.95", description:"Countertop convection oven with air fryer."},
        {title:"KitchenAid Artisan Tilt-Head Stand Mixer", url:"https://amzn.to/3HHSZmj", price:"$379.99", description:"Versatile stand mixer for baking."},
        {title:"Cuisinart 14-Cup Food Processor", url:"https://amzn.to/4fKXKs0", price:"$149.95", description:"Powerful food processor for chopping and slicing."},
        {title:"Ninja Foodi 9-in-1 Pressure Cooker and Air Fryer", url:"https://amzn.to/3V6wKcS", price:"$199.99", description:"Multi-cooker with air frying and pressure cooking features."},
        {title:"NutriBullet Pro High-Speed Blender/Mixer System", url:"https://amzn.to/4mOUwG5", price:"$89.99", description:"Compact blender for smoothies and shakes."},
        {title:"Hydro Flask Stainless Steel Water Bottle", url:"https://amzn.to/475gmRe", price:"$39.95", description:"Vacuum insulated bottle keeps drinks cold or hot."}
    ],
    Tech: [
        {title:"Apple AirPods Pro (2nd Generation)", url:"https://amzn.to/3UAYMx7", price:"$249.00", description:"Premium ANC, deep spatial audio, seamless Apple ecosystem, and excellent build quality."},
        {title:"Samsung Galaxy Buds FE (Fan Edition)", url:"https://amzn.to/4m6BhIh", price:"$99.99", description:"Reliable ANC, auto device switching, and balanced audio for Android users."},
        {title:"Anker Soundcore P20i", url:"https://amzn.to/4mqytoV", price:"$29.99", description:"Budget-friendly wireless earbuds with decent ANC and comfort."},
        {title:"Samsung T7 Portable SSD 1TB", url:"https://amzn.to/3J1xAor", price:"$139.99", description:"Fast external solid state drive."},
        {title:"Logitech MX Master 3S Wireless Mouse", url:"https://amzn.to/4oFWA4T", price:"$99.99", description:"Ergonomic wireless mouse with customizable buttons and high-precision tracking."},
        {title:"Sony WH-1000XM4 Wireless Noise-Canceling Headphones", url:"https://amzn.to/3V5ToC2", price:"$199.99", description:"Industry-leading noise-canceling headphones with long battery life and touch controls."},
        {title:"Kindle Paperwhite (2024)", url:"https://amzn.to/4mTKZOd", price:"$159.99", description:"Waterproof e-reader with high-resolution 7-inch display and adjustable warm light."}
    ],
    Outdoors: [
        {title:"Coleman Sundome Tent", url:"https://amzn.to/4myC9oX", price:"$99.99", description:"Easy setup tent for camping."},
        {title:"LifeStraw Personal Water Filter", url:"https://amzn.to/4m3CoIw", price:"$19.97", description:"Portable water purifier for outdoor use."},
        {title:"Etekcity Lantern Camping Lantern", url:"https://amzn.to/41JMmqq", price:"$23.99", description:"LED lantern with adjustable brightness."},
        {title:"Osprey Atmos AG Backpack", url:"https://amzn.to/3Jngwtq", price:"$260.00", description:"Comfortable hiking backpack with ventilation."},
        {title:"Garmin GPSMAP Handheld GPS Navigator", url:"https://amzn.to/45BCoJX", price:"$399.99", description:"Rugged GPS device for outdoor navigation."}
    ],
    Household: [
        {title:"iRobot Roomba 694 Robot Vacuum", url:"https://amzn.to/4flpTp8", price:"$249.99", description:"Smart robot vacuum for home cleaning."},
        {title:"Dyson V8 Absolute Cordless Vacuum Cleaner", url:"https://amzn.to/4fll1QY", price:"$399.99", description:"Powerful cordless vacuum cleaner."},
        {title:"Instant Pot Duo Crisp Pressure Cooker and Air Fryer", url:"https://amzn.to/3J1ZhxC", price:"$159.99", description:"Multi-use pressure cooker with air fryer lid."},
        {title:"Philips Hue White and Color Ambiance Smart Bulb", url:"https://amzn.to/3JhsKUq", price:"$49.99", description:"Smart LED bulb with app control."},
        {title:"Nespresso Vertuo Coffee and Espresso Maker", url:"https://amzn.to/3HKisLX", price:"$199.00", description:"Single serve coffee and espresso machine."}
    ],
    HomeDecor: [
        {title:"KARMA AND LUCK Calming Spirit Amethyst Crystal Feng Shui Tree of Life", url:`https://www.amazon.com/dp/B0B8QWN9NT?tag=${AFFILIATE_TAG}`, price:"$39.95", description:"A handcrafted amethyst crystal tree symbolizing peace and spiritual growth."},
        {title:"Linon Brooklyn Sherpa Office Chair, Ivory", url:`https://www.amazon.com/dp/B083TRV28M?tag=${AFFILIATE_TAG}`, price:"$129.99", description:"Ivory sherpa upholstered office chair with adjustable height and silver base."},
        {title:"Jersey Home Decor Wall Waterfall XL 47\" Wide x 24\" Tall", url:`https://www.amazon.com/dp/B01KP0ONSY?tag=${AFFILIATE_TAG}`, price:"$399.99", description:"Large wall-mounted waterfall feature that adds a tranquil ambiance."},
        {title:"Medify MA-40 Air Purifier with True HEPA H13 Filter", url:`https://www.amazon.com/dp/B07LGDYV3C?tag=${AFFILIATE_TAG}`, price:"$249.99", description:"Air purifier covering up to 1,793 sq ft with HEPA H13 filter."},
        {title:"Kyzfy 24.4-Inch Relaxing Liquid Motion Lamp", url:`https://www.amazon.com/dp/B0DRBZS1DR?tag=${AFFILIATE_TAG}`, price:"$44.95", description:"Soothing liquid motion lamp with vibrant colors for relaxation."},
        {title:"VIAHART 14\" Glass Mini Aquarium", url:`https://www.amazon.com/dp/B0CRDP8TM9?tag=${AFFILIATE_TAG}`, price:"$69.99", description:"Compact glass mini aquarium for tabletop decoration and fish keeping."}
};

const categorySelect = document.getElementById('categorySelect');
const productSelect = document.getElementById('productSelect');
const productDetails = document.getElementById('productDetails');

categorySelect.addEventListener('change', () => {
    const cat = categorySelect.value;
    productSelect.innerHTML = '<option value="">Select a product</option>';
    productDetails.innerHTML = '';
    if(!cat){ productSelect.disabled = true; return; }
    productSelect.disabled = false;
    PRODUCTS[cat].forEach((p, idx) => {
        const opt = document.createElement('option');
        opt.value = idx;
        opt.textContent = p.title;
        productSelect.appendChild(opt);
    });
});

productSelect.addEventListener('change', () => {
    const cat = categorySelect.value;
    const idx = productSelect.value;
    if(idx === "") { productDetails.innerHTML = ''; return; }
    const p = PRODUCTS[cat][idx];
    const finalURL = applyAffiliate(p.url);
    productDetails.innerHTML = `
        <div class="product-info category-${cat}">
            <strong>${p.title}</strong><br>
            Price: ${p.price}<br>
            <a href="${finalURL}" target="_blank">Buy Here</a><br>
            Description: ${p.description}<br>
            <span class="more-info" onclick="moreInfo('${p.title}','${p.description}')">More Information</span>
            <div id="aiDesc" style="margin-top:5px; font-style:italic;"></div>
        </div>
    `;
    moreInfo(p.title, p.description, true);
});

function moreInfo(title, desc, auto=false){
    puter.ai.chat(`Provide a more detailed description of: ${title}. Current description: ${desc}`)
    .then(response => {
        if(auto){
            document.getElementById('aiDesc').textContent = response;
        } else {
            puter.print(response);
        }
    });
}
</script>
</body>
</html>
