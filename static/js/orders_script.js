window.onload = function () {
    let quantity_arr = []
    let price_arr = []

    const order_total_quantity_view = document.querySelector('.order_total_cost')
    const order_total_cost_view = document.querySelector('.order_total_cost')

    let total_forms = parseInt(document.querySelector('input[name="orderitems-TOTAL_FORMS"]').value)
    let order_total_quantity = parseInt(document.querySelector('.order_total_quantity').innerHTML || 0)
    let order_total_cost = parseFloat(document.querySelector('.order_total_cost').innerHTML || 0)
    
    orderSummaryUpdate()

    document.querySelectorAll('input[type="number"]').forEach(elem => {
        elem.addEventListener('change', () => {
            orderSummaryUpdate()
        })
    })

    document.querySelectorAll('input[type="checkbox"]').forEach(elem => {
        elem.addEventListener('change', () => {
            orderSummaryUpdate()
        })
    })

    document.querySelectorAll('select').forEach(elem => {
        elem.addEventListener('change', function () {
            let target = event.target
            product_id = this.options[this.selectedIndex].value
            url = "http://127.0.0.1:8000/api/product?id=" + product_id
            fetch(url)
                .then(response => response.json())
                .then(json => {
                    let index = parseInt(target.name.replace('orderitems-', '').replace('-product', ''))
                    let price_name = 'orderitems-' + index + '-price'
                    let quantity_name = 'orderitems-' + index + '-quantity'
                    document.querySelector(`input[name="${price_name}"]`).value = json.price
                    document.querySelector(`input[name="${quantity_name}"]`).value = 0
                    orderSummaryUpdate()
                })
                .catch(err => {console.log(err)})
        })
    })

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        for (let i=0; i < total_forms; i++) {
            let delete_checked = document.querySelector(`input[name="orderitems-${i}-DELETE"]`).checked
            if (!delete_checked) {
                let quantity = parseInt(document.querySelector('input[name="orderitems-' + i + '-quantity"]').value)
                let price = parseFloat(document.querySelector('input[name="orderitems-' + i + '-price"]').value)
                quantity_arr[i] = quantity
                price_arr[i] = price || 0
            } else {
                quantity_arr[i] = 0
            }
        }

        order_total_quantity = quantity_arr.reduce((a,b) => a + b, 0)
        order_total_cost = quantity_arr.reduce((a,b,i) => a + (b * price_arr[i]), 0)
        order_total_quantity_view.innerHTML = order_total_quantity
        order_total_cost_view.innerHTML = order_total_cost.toFixed(2)
    }
}