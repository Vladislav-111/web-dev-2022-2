var ModalDelElement = document.getElementById('delete-book')
ModalDelElement.addEventListener('show.bs.modal', function (event){
    let url = event.relatedTarget.dataset.url;
    let form = this.querySelector('form');
    form.action = url;
    let bookName = document.getElementById('book-name');
    bookName.innerHTML = event.relatedTarget.closest('p').querySelector('.book-name').value
})