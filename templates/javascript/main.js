function copyId(id) {
    navigator.clipboard.writeText(id)
    .then(text => {
      alert('ID скопирован')
    })
    .catch(err => {
      alert('Что-то пошло не так, повторите попытку позже')
    })
}

