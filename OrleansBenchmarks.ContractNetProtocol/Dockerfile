FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base
USER $APP_UID
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["OrleansBenchmarks.ContractNetProtocol/OrleansBenchmarks.ContractNetProtocol.csproj", "OrleansBenchmarks.ContractNetProtocol/"]
RUN dotnet restore "OrleansBenchmarks.ContractNetProtocol/OrleansBenchmarks.ContractNetProtocol.csproj"
COPY . .
WORKDIR "/src/OrleansBenchmarks.ContractNetProtocol"
RUN dotnet build "OrleansBenchmarks.ContractNetProtocol.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "OrleansBenchmarks.ContractNetProtocol.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
COPY --from=build /app/build .
ENTRYPOINT ["dotnet", "OrleansBenchmarks.ContractNetProtocol.dll"]
