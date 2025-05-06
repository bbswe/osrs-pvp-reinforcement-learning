#!/bin/bash
# Script to copy all models from ThreadParallel to RayM2Pro and make them trainable

# Directory paths
SOURCE_DIR="pvp-ml/experiments/ThreadParallel/models"
TARGET_DIR="pvp-ml/experiments/RayM2Pro/models"
BACKUP_DIR="pvp-ml/experiments/RayM2Pro/models_full_backup"

# Create backup of current RayM2Pro models
echo "Creating backup of current RayM2Pro models..."
mkdir -p "$BACKUP_DIR"
cp -p "$TARGET_DIR"/*.zip "$BACKUP_DIR/" 2>/dev/null || echo "No existing models to backup"

# Get timestamp for changelog
TIMESTAMP=$(date "+%b %d, %Y - %H:%M %Z")
echo "Running model migration at $TIMESTAMP"

# Count total models to copy
TOTAL_MODELS=$(find "$SOURCE_DIR" -name "*.zip" | wc -l)
echo "Found $TOTAL_MODELS models to copy from ThreadParallel"

# Create directory for temporary files
TEMP_DIR="pvp-ml/experiments/RayM2Pro/models_temp"
mkdir -p "$TEMP_DIR"

# Copy and convert models
COUNT=0
COPIED=0
FAILED=0

echo "Starting copy and conversion process..."
for MODEL in $(find "$SOURCE_DIR" -name "*.zip" | sort); do
    MODEL_FILENAME=$(basename "$MODEL")
    COUNT=$((COUNT + 1))
    
    # Skip if model already exists in target
    if [ -f "$TARGET_DIR/$MODEL_FILENAME" ]; then
        echo "[$COUNT/$TOTAL_MODELS] Model $MODEL_FILENAME already exists in target directory, skipping"
        continue
    fi

    echo "[$COUNT/$TOTAL_MODELS] Processing $MODEL_FILENAME"
    
    # Copy the model file
    cp -p "$MODEL" "$TARGET_DIR/" || { echo "Failed to copy $MODEL_FILENAME"; FAILED=$((FAILED + 1)); continue; }
    
    # Convert non-trainable model to trainable if needed
    if pvp-ml/env/bin/python -c "import torch; checkpoint = torch.load('$TARGET_DIR/$MODEL_FILENAME', map_location='cpu'); exit(0 if 'optimizer' in checkpoint else 1)" 2>/dev/null; then
        echo "[$COUNT/$TOTAL_MODELS] Model $MODEL_FILENAME is already trainable"
    else
        echo "[$COUNT/$TOTAL_MODELS] Converting $MODEL_FILENAME to trainable format"
        if pvp-ml/env/bin/python convert_model.py --input-model "$TARGET_DIR/$MODEL_FILENAME" --output-model "$TEMP_DIR/$MODEL_FILENAME-trainable.zip"; then
            mv "$TEMP_DIR/$MODEL_FILENAME-trainable.zip" "$TARGET_DIR/$MODEL_FILENAME"
            echo "[$COUNT/$TOTAL_MODELS] Successfully converted $MODEL_FILENAME to trainable format"
        else
            echo "[$COUNT/$TOTAL_MODELS] Failed to convert $MODEL_FILENAME to trainable format"
            FAILED=$((FAILED + 1))
            continue
        fi
    fi
    
    COPIED=$((COPIED + 1))
    
    # Show progress every 10 models
    if [ $((COUNT % 10)) -eq 0 ]; then
        echo "Progress: $COUNT/$TOTAL_MODELS models processed ($COPIED copied, $FAILED failed)"
    fi
done

# Cleanup
rm -rf "$TEMP_DIR"

echo "Copy complete! Copied $COPIED models, $FAILED failures"
echo "You now have a full history of models in $TARGET_DIR"
echo ""
echo "Consider updating CHANGELOG.md with:"
echo "## $TIMESTAMP"
echo ""
echo "### Migrated Full Model History from ThreadParallel to RayM2Pro"
echo "- Copied $COPIED model checkpoints from ThreadParallel to RayM2Pro experiment"
echo "- Converted all models to trainable format for Ray compatibility"
echo "- Enabled complete past self-play with full model history"
echo "- Eliminated 'missing league opponent' warnings during training"
echo "- Preserved entire training evolution history for better opponent selection" 