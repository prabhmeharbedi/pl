@echo off
setlocal

REM Configuration with the correct project ID
set PROJECT_ID=835103152018
set SERVICE_NAME=loopot
set REGION=us-central1

cd ..
echo Running prepare_deploy script to copy framework files...
call prepare_deploy.bat

echo Building and deploying to Google Cloud Run...
echo Project: %PROJECT_ID%
echo Service: %SERVICE_NAME%
echo Region: %REGION%

REM Build container image using Cloud Build
echo Building container image...
gcloud builds submit --tag gcr.io/%PROJECT_ID%/%SERVICE_NAME% .

REM Deploy to Cloud Run
echo Deploying to Cloud Run...
gcloud run deploy %SERVICE_NAME% ^
  --image gcr.io/%PROJECT_ID%/%SERVICE_NAME% ^
  --platform managed ^
  --region %REGION% ^
  --allow-unauthenticated

echo Deployment complete!
for /f "tokens=*" %%a in ('gcloud run services describe %SERVICE_NAME% --region %REGION% --format "value(status.url)"') do (
  echo Your service is available at: %%a
) 