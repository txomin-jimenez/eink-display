#!/bin/bash
# convert to grayscale 600x800 png portrait image. if image is landscape, crop image taking people faces into account
INPUT_FILENAME=$1
TEMP_FILENAME="temp.png"

create_temp_image_from()
{
  source_image=$1
  cp $source_image $TEMP_FILENAME
}

get_image_width()
{
  width_result=$(identify -format \"%W\" $TEMP_FILENAME)
  width="${width_result%\"}"
  echo "${width#\"}"
}

get_image_height()
{
  height_result=$(identify -format \"%H\" $TEMP_FILENAME)
  height="${height_result%\"}"
  echo "${height#\"}"
}

get_image_orientation()
{
  echo $(identify -format \"%[EXIF:orientation]\" $TEMP_FILENAME)
}

rotate_image()
{
  degrees=$1
  mogrify -rotate "$degrees" $TEMP_FILENAME
}

fix_image_orientation()
{
  top_left=1
  left_bottom=8
  bottom_right=3
  right_top=6
  orientation=$(get_image_orientation)
  orientation="${orientation%\"}"
  orientation="${orientation#\"}"
  case $orientation in
  $top_left)
    echo top_left
  ;;
  $left_bottom)
    echo left_bottom
    rotate_image "-90"
  ;;
  $bottom_right)
    echo bottom_right
    rotate_image "-180"
  ;;
  $right_top)
    echo right_top
    rotate_image "90"
  ;;
  esac
 }

calc_aspect_ratio()
{
  width=$1
  height=$2
  echo $(echo "$width / $height" | bc -l)
}

round()
{
  echo $(printf %.$2f $(echo "scale=$2;(((10^$2)*$1)+0.5)/(10^$2)" | bc))
};

resize_landscape()
{
  aspect_ratio=$1
  new_width=$(echo "800*$aspect_ratio" | bc)
  new_width=$(round $new_width 0)

  mogrify -resize ${new_width}x800 $TEMP_FILENAME

  echo $new_width
}

calc_image_center()
{
  width=$1
  image_center=$(echo "$width/2" | bc)
  face_x=$(facedetect --center $TEMP_FILENAME)
  if [[ ! -z $face_x ]]; then
    face_x=($face_x)
    face_x=${face_x[0]}
    echo $(($face_x - 300))
  else
    echo $(($image_center - 300))
  fi
}

crop_landscape()
{
  width=$1
  crop_x=$(calc_image_center $width)
  echo 600x800+${crop_x}+0
  mogrify -crop 600x800+${crop_x}+0 $TEMP_FILENAME
}

resize_portrait()
{
  aspect_ratio=$1
  new_height=$(echo "600/$aspect_ratio" | bc)
  mogrify -resize 600x${new_height} $TEMP_FILENAME
}

convert_to_grayscale()
{
  mogrify -colorspace Gray $TEMP_FILENAME
  mogrify -auto-gamma $TEMP_FILENAME
  mogrify -auto-level $TEMP_FILENAME
}

save_output()
{
  # overwrite
  rm $INPUT_FILENAME
  mv $TEMP_FILENAME $INPUT_FILENAME
}

create_temp_image_from $INPUT_FILENAME
fix_image_orientation
width=$(get_image_width)
height=$(get_image_height)
aspect_ratio=$(calc_aspect_ratio $width $height)

echo $width x $height - $aspect_ratio
if [[ $(echo "$aspect_ratio > 1" | bc -l) -eq 1 ]]; then
  echo "landscape"
  new_width=$(resize_landscape $aspect_ratio)
  crop_landscape $new_width
else
  echo "portrait"
  resize_portrait $aspect_ratio
fi
convert_to_grayscale
save_output