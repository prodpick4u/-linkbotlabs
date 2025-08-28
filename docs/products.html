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

// Multi-affiliate URL application
function applyAffiliate(url){
    try {
        const ref = document.referrer;
        if(ref.includes("starter")) {
            if(url.includes("amazon.com") && !url.includes(`tag=${AFFILIATE_TAG}`)){
                return url.includes("?") ? `${url}&tag=${AFFILIATE_TAG}` : `${url}?tag=${AFFILIATE_TAG}`;
            }
        }
    } catch(e){}
    return url;
}

// TEMU + Fallback Products
const PRODUCTS = {
    Health: [
        {title:"Fitbit Charge 5", url:"https://amzn.to/45zc4k1", price:"$129.95", description:"Fitness tracker with built-in GPS and health metrics."},
        {title:"Theragun Elite", url:"https://amzn.to/463BPYL", price:"$299.00", description:"Percussive therapy device for muscle recovery."},
        {title:"Methylene Blue", url:"https://amzn.to/4ldkJwL", price:"Varies", description:"Supplement for mitochondrial support."},
        {title:"Irish Sea Moss", url:`https://www.amazon.com/dp/B0CTMJYZ73?tag=${AFFILIATE_TAG}`, price:"Varies", description:"Supports immune and thyroid health."},
        {title:"Shilajit", url:"https://amzn.to/4li6vuC", price:"Varies", description:"Boosts energy and vitality."}
    ],
    Beauty: [
        {title:"Revlon Hair Dryer Brush", url:"https://amzn.to/3HIHhrw", price:"$59.99", description:"Hair styling tool for drying and volumizing."},
        {title:"Olay Regenerist Cream", url:"https://amzn.to/3HwMhQ8", price:"$25.99", description:"Anti-aging facial moisturizer."},
        {title:"Neutrogena Wipes", url:"https://amzn.to/3UAEOSX", price:"$9.99", description:"Gentle makeup remover wipes."},
        {title:"Maybelline Mascara", url:"https://amzn.to/4oHMpgn", price:"$7.99", description:"Volumizing mascara with buildable formula."},
        {title:"CeraVe Cleanser", url:"https://amzn.to/4mI68uu", price:"$14.99", description:"Gentle facial cleanser for dry skin."}
    ],
    Kitchen: [
        {title:"Instant Pot Duo", url:"https://amzn.to/4oLDhqU", price:"$89.00", description:"7-in-1 multi-functional pressure cooker."},
        {title:"Lodge Cast Iron Skillet", url:"https://amzn.to/4oKl7WG", price:"$24.99", description:"Durable pre-seasoned cast iron pan."},
        {title:"Breville Smart Oven Air Fryer", url:"https://amzn.to/47BJoYI", price:"$279.95", description:"Countertop convection oven with air fryer."},
        {title:"KitchenAid Stand Mixer", url:"https://amzn.to/3HHSZmj", price:"$379.99", description:"Versatile mixer for baking."}
    ],
    Tech: [
        {title:"Apple AirPods Pro 2nd Gen", url:"https://amzn.to/3UAYMx7", price:"$249.00", description:"Premium ANC earbuds with deep spatial audio."},
        {title:"Samsung Galaxy Buds FE", url:"https://amzn.to/4m6BhIh", price:"$99.99", description:"Reliable ANC earbuds for Android."},
        {title:"Anker Soundcore P20i", url:"https://amzn.to/4mqytoV", price:"$29.99", description:"Budget wireless earbuds."}
    ],
    Outdoors: [
        {title:"Coleman Sundome Tent", url:"https://amzn.to/4myC9oX", price:"$99.99", description:"Easy setup camping tent."},
        {title:"LifeStraw Water Filter", url:"https://amzn.to/4m3CoIw", price:"$19.97", description:"Portable water purifier."}
    ],
    Household: [
        {title:"iRobot Roomba 694", url:"https://amzn.to/4flpTp8", price:"$249.99", description:"Smart robot vacuum."},
        {title:"Dyson V8 Vacuum", url:"https://amzn.to/4fll1QY", price:"$399.99", description:"Powerful cordless vacuum."}
    ],
    HomeDecor: [
        {title:"Amethyst Crystal Tree", url:`https://www.amazon.com/dp/B0B8QWN9NT?tag=${AFFILIATE_TAG}`, price:"$39.95", description:"Handcrafted crystal tree symbolizing peace."},
        {title:"Linon Sherpa Office Chair", url:`https://www.amazon.com/dp/B083TRV28M?tag=${AFFILIATE_TAG}`, price:"$129.99", description:"Ivory sherpa office chair."}
    ],
    Kitchen_TEMU: [
        {title:"Multi Rice Cooker", url:"https://share.temu.com/jwZL6Tbh2SB", price:"Check Temu UK", description:"Versatile rice cooker."},
        {title:"Foldable Kettle", url:"https://share.temu.com/GZe6nSeHcEB", price:"Check Temu UK", description:"Compact foldable kettle."}
    ]
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
    Object.keys(PRODUCTS).forEach(key => {
        if(key === cat || key.startsWith(cat+"_")) {
            PRODUCTS[key].forEach((p, idx) => {
                const opt = document.createElement('option');
                opt.value = key + "|" + idx;
                opt.textContent = p.title;
                productSelect.appendChild(opt);
            });
        }
    });
});

productSelect.addEventListener('change', () => {
    const val = productSelect.value;
    if(!val){ productDetails.innerHTML = ''; return; }
    const [cat, idx] = val.split("|");
    const p = PRODUCTS[cat][parseInt(idx)];
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
