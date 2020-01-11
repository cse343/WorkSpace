FROM java:8
EXPOSE 8080
ADD /deploy/settings.jar settings.jar
ENTRYPOINT ["java","-jar","settings.jar"]