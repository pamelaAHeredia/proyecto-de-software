const btnDelete = document.querySelectorAll('.btn-dange')

if(btnDelete){
    const btnArray = Array.from(btnDelete); 
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if(!confirm('Está seguro de que desea eliminarlo?')){
                e.preventDefault()
            }
        })
    })
}