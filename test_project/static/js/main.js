// Get SearchForm and Page links
let searchform =  document.getElementById('searchForm')
let pagelinks = document.getElementsByClassName('page-link')

// Make sure that the search form actually exists
if(searchform){

       /*
        * Now what we wanna do is loop through every single item and add an eventHandler.
        * So all the pageLinks we are gonna have in eventHandler, basically allow us to do something 
        * when tht page item is clicked on.  
        */

     for (let i=0;pagelinks.length > i;i++)
        {
            pagelinks[i].addEventListener('click', function (e){
                e.preventDefault()
                
                // Get the Data Attribute
                let page = this.dataset.page
                
                // Add hidden search input to the form
                searchform.innerHTML += `<input value=${page} name="page" hidden/>`

                // Submit Form
                searchform.submit()
            }) 
        }

    /*
     * Once you test this code you will find that the page, isn't changing as per the pagination, and in the console
     * and we will find rather "Button clicked" being printed on the cosnole.
     */
}