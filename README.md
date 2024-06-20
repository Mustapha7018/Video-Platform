# 📹 Video Platform
A bespoke video hosting platform `(Veedeo Platform)` for Paul Leonard, tailored to his business needs. This platform allows video creators to upload, share, and manage videos seamlessly. 


## 🎯 Project Objective
Paul Leonard needed a dedicated video platform to host his content without the branding issues present in other video hosting services. This project delivers a custom solution tailored to his brand.


## 🛠 Features
--- User Features ---
- 🔑 Signup & Login: Users can register and log in using email and password. Includes account verification and password recovery.
- 📹 Video Navigation: Users can easily navigate between video pages.
- 🔗 Share Videos: Users can share video links across different pages.

--- Admin Features ---
- ⬆️ Upload Videos: Admins can upload videos with titles and descriptions.
- ⚙️ Manage Videos: Admins can edit and delete videos.

--- Video Page ---
- 🖼 Single Video Display: Each page presents one video.
- ⏭ Navigation: Includes next and previous buttons to navigate between videos. Buttons hide when no further videos are available.
- ⏯ Control Buttons: Common video control buttons for user convenience.
- 📛 Brand Logo: Prominently displays the business logo at the top.
- 🔗 Share Button: Allows users to share the video page link.


## 📋 Deliverables
- Source Code: Available  here on [GitHub](https://github.com/Mustapha7018/Video-Platform) with a well-written README.
- ER Diagram: Included in the repository.
- Deployed Link: [veedeo.pythonanywhere.com](https://veedeo.pythonanywhere.com/)


## 📐 ER Diagram Description
- User
  * id: Primary Key
  * email: Unique Email
  * password: Hashed Password
  * is_staff: Boolean (indicates if the user is an admin)

- Video
  * id: Primary Key
  * title: String
  * description: Text
  * thumbnail: URL/Image Path
  * video_file: URL/File Path
  * uploaded_by: Foreign Key to User
  * uploaded_at: DateTime


## 🚀 Getting Started
### Prerequisites
- Python 3.x
- Django 5.x
- Other dependencies listed in `requirements.txt`

### Installation
1. Clone the repository
```
git clone https://github.com/Mustapha7018/Video-Platform.git
```
2. Navigate to the project directory
```
cd Video-Platform
```
3. Install dependencies
```
pip install -r requirements.txt
```

### Running the Application
1. Apply Migrations:
```
python manage.py migrate
```
2. Create a superuser for admin access:
```
python manage.py createsuperuser
```
3. Run the development server:
```
python manage.py runserver
```
4. Access the application at `http://127.0.0.1:8000`.


## 🧪 Unit Tests
### Running Unit Tests
To ensure the integrity of the application, unit tests have been written to cover various functionalities. To run the unit tests, use the following command:
```
python manage.py test
```

## 🛠️ Django Workflow
### GitHub Actions
The project uses GitHub Actions for Continuous Integration (CI). The workflow is defined in the `.github/workflows/video-tests.yml` file. This setup ensures that tests are automatically run on each push and pull request to the repository.

### Setting Up Github Actions
1. Ensure the `.github/workflows/django.yml` file is present in the repository.
2. The workflow will automatically trigger on pushes and pull requests to the repository, running the specified tests and checks.
3. This integration helps maintain code quality and streamline the development process.


## 📊 ER DIAGRAM
![image](https://github.com/Mustapha7018/Video-Platform/assets/91817013/68eb89d9-efb7-4ba6-a6f6-0980b8b3fa29)

