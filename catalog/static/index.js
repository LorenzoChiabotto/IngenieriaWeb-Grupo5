tagsSelected = []
tagsList = $('#id_tags');
tagsDiv = document.getElementById('tagsContainer');
form = document.getElementsByTagName('form')[0];


tagsList.on('change', function(){ 
    tag = tagsList.find('option[value=' + this.value + ']');
    console.log(this.value)
    valueSelected = this.value
    labelSelected = tag.text()
    

    if(!valueSelected){
        return
    }
    tagsSelected.push(valueSelected)

    pillDiv = document.createElement('div')
    pillDiv.className = 'badge badge-pill badge-primary p-0 m-1'
    aRef = document.createElement('a')
    aRef.className = 'text-decoration-none text-white m-3'
    aRef.appendChild(document.createTextNode(labelSelected))

    cancelButton = document.createElement('button')
    cancelButton.className ='h-100 w-wrap rounded-right rounded-lg bg-light btn-sm btn border border-primary'
    cancelButton.id = valueSelected
    spanCancelButton = document.createElement('span', {
        'aria-hidden':'true',
    })

    spanCancelButton.appendChild(document.createTextNode('X'))
    cancelButton.appendChild(spanCancelButton)
    pillDiv.appendChild(aRef)
    pillDiv.appendChild(cancelButton)
    
     cancelButton.addEventListener('click', function(e){
        event.preventDefault();
        elementSelected = this.id
        $('#id_tags > [value='+elementSelected+']').attr("hidden", false)
        $('#id_tags > [value='+elementSelected+']').prop("selected", false);
        //tagsList.getElementById(elementSelected).setAttribute
        //console.log($('#id_tags > [value='+elementSelected+']').)
        this.closest('div').remove()
    })

    tagsDiv.appendChild(pillDiv)
    
    tag.attr("hidden", true)
  });


  /*
  <div class="badge badge-pill badge-primary p-0 m-1"> 
                    <a href="#" class="text-decoration-none text-white m-3">Primary </a>
                    <button class="h-100 w-wrap rounded-right rounded-lg bg-light btn-sm btn border border-primary">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>


                
      var formData = new FormData(document.querySelector('form'))
      console.log(formData.get('tags'))
      tagsList = document.getElementById('tags').value = tagsSelected;
      formData.set('tags',tagsSelected)
      console.log(formData)
      console.log(formData.getAll("tags"))
      console.log(formData.get('description'))
      formData.set('description','new descriptionnnnnn')
      console.log(formData.get('description'))



        form.addEventListener('submit',(event) => {
      console.log(tagsSelected)
      tagsList.value = tagsSelected
      tagsList.set('tags',tagsSelected)
      console.log(tagsList)
      debugger
    })

  */