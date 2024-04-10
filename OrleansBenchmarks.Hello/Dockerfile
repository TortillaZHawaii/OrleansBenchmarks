FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base
ARG BUILD_CONFIGURATION=Release
ARG PROJECT_NAME=OrleansBenchmarks.Hello

WORKDIR /src
COPY . .

RUN dotnet restore "${PROJECT_NAME}/${PROJECT_NAME}.csproj"

WORKDIR "/src/${PROJECT_NAME}"
RUN dotnet build "${PROJECT_NAME}.csproj" -c $BUILD_CONFIGURATION -o /src/bin
RUN dotnet publish "${PROJECT_NAME}.csproj" -c $BUILD_CONFIGURATION -o /src/bin/publish /p:UseAppHost=false

WORKDIR /src/bin/publish
ENTRYPOINT ["dotnet", "${PROJECT_NAME}.dll"]
