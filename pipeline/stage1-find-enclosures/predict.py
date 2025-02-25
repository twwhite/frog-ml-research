# Find bounding box of actual enclosures in the image
# Standardize a meta-bounding box by finding the centroid of each and expanding by a pos. and neg. delta in x and y
# Need to be sure that the meta-bounding box is large enough to contain the enclosures,
# Need to be sure that the meta-bounding box still fits within the frame (can offset by delta away from frame minmax dims)

# In this stage we will do all of the cropping/resizing/frame dropping/etc.
