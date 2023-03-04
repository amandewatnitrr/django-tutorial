<strong>
<p align="justify">

# Getting started with Django

![](imgs/1*Y0l-VVKTsvhv5zmSmTRJTQ.gif)

- Django is a python based Web-framework and it is a backend framework.
- THis means we can use python to build websites.
- It is more of a heavy weight framework. So, it uses a batteries included approach. That means it really is more opinionated in how you build out your application.
- It uses MVC(Model View Controller) design pattern for Django, it's model view template.
- Building API's with Django is easy. If we want to build a mobile App or use some kind of frontend framework, weneed some API data.
- Django makes it very easy, Django has something called The REST API Framework which is built on top of Django and The REST Framework helps you build REST APIs.
- Django follows the MVT structure, There's a model view control structure, which a lot of us from other frameworks may be familiar with.
- Django takes care of the controller aspect of things.

## MVT (Model View Template) Design Pattern

- The Mode is the Data Access Layer, this going to be our database tables built out in classes.
- Templates is the presentation layer . This is what the user will see.
- The View is the business logic.
- So, for wxample when we go to a certain website they are going to go through some of the URLs, we're gonna find the URLs that matches some kind of function in the backend and that's going to be our views.
- Those Views right there in the views layer that's gonna go ahead and get some data probably from the models and it's going to render some kind of template to us and we send that back to the user, that's the flow here.
- We're requesting data, the views, the business logic, and we just get this and send it back to the user. So, that's about MVTdesign pattern which is very much similar to MVC

    ``` Mermaid
        flowchart LR
            A[[Website]] --> B[[URLs]]
            B[[URLs]] --> A[[Website]]
            B[[URLs]] -- HTTP Response --> C[[Views]]
            C[[Views]] -- HTTP Request --> B[[URLs]]
            C[[Views]] -..-> D[[Models]]
            D[[Models]] -..-> C[[Views]]
            C[[Views]] -..-> E[[Templates]]
            E[[Templates]] -..-> C[[Views]]
    ```

## What is a framework??

- Web-framework is simply a collection of modules, packages and libraries designed to speed-up development.
- Django already reconfigures a lot of things for us. It is strongly recommended and advised against you hand coding absolutely everything by yourself.
- There are various other backend frameworks that are openly available which include <img src="https://img.shields.io/badge/NodeJs-339933?style=plastic&logo=Node.Js&logoColor=white"/>, <img src="https://img.shields.io/badge/PHP-777BB4?style=plastic&logo=PHP&logoColor=white"/>, <img src="https://img.shields.io/badge/Laravel-FF2D20?style=plastic&logo=Laravel&logoColor=white"/> and <img src="https://img.shields.io/badge/Express-000000?style=plastic&logo=Express&logoColor=white"/>.

- There are other Python Frameworks as well which include <img src="https://img.shields.io/badge/Flask-000000?style=plastic&logo=Flask&logoColor=white"/>, <img src="https://img.shields.io/badge/CherryPie-000000?style=plastic&logo=CherryPie&logoColor=white"/>, <img src="https://img.shields.io/badge/Web2Py-8DD6F9?style=plastic&logo=WebPack&logoColor=black"/> and <img src="https://img.shields.io/badge/Pyramid-000000?style=plastic&logo=Pyramid&logoColor=white"/>

</p>
</strong>
