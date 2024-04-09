FROM mcr.microsoft.com/dotnet/runtime:8.0 AS base
USER $APP_UID
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["OrleansBenchmarks.Hello/OrleansBenchmarks.Hello.csproj", "OrleansBenchmarks.Hello/"]
RUN dotnet restore "OrleansBenchmarks.Hello/OrleansBenchmarks.Hello.csproj"
COPY . .
WORKDIR "/src/OrleansBenchmarks.Hello"
RUN dotnet build "OrleansBenchmarks.Hello.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "OrleansBenchmarks.Hello.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "OrleansBenchmarks.Hello.dll"]
