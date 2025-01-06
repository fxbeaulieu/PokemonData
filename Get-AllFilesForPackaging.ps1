$options = ""
$pokemon_data_file = Get-Item -Path ".\data\pokemon.csv"
$type_chart_data_file = Get-Item -Path ".\data\type-chart.yaml"
$img_files = Get-ChildItem -Path ".\data\img" -Filter ".png"
$script_file = Get-Item -Path ".\get_quick_types_stats.py"
$ico_file = Get-Item -Path ".\pokedex.ico"

# Add data files
foreach ($file in @($pokemon_data_file,$type_chart_data_file)) {
    $options += "--add-data '" + $file.FullName + ";data' "
}

# Add image files
foreach ($file in $img_files) {
    $options += "--add-data '" + $file.FullName + ";data\\img' "
}

$options += "--add-data '" + $ico_file.FullName + ";.' "

$command = "pyinstaller --onefile  --noconsole --icon='.\\pokedex.ico' " + $options + $script_file.Name
Invoke-Expression $command
