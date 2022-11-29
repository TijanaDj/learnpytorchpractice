"""
Contains functionality for creating PyTorch DataLoaders for 
image classification data.
"""
import os
import torch

from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torch.utils.data import random_split
NUM_WORKERS = os.cpu_count()

def create_dataloaders(
    train_dir: str, 
    test_dir: str, 
    transform: transforms.Compose, 
    batch_size: int, 
    num_workers: int=NUM_WORKERS
):
  """Creates training and testing DataLoaders.

  Takes in a training directory and testing directory path and turns
  them into PyTorch Datasets and then into PyTorch DataLoaders.
  
  Also, I made a change so it takes small amount of data.

  Args:
    train_dir: Path to training directory.
    test_dir: Path to testing directory.
    transform: torchvision transforms to perform on training and testing data.
    batch_size: Number of samples per batch in each of the DataLoaders.
    num_workers: An integer for number of workers per DataLoader.

  Returns:
    A tuple of (train_dataloader, test_dataloader, class_names).
    Where class_names is a list of the target classes.
    Example usage:
      train_dataloader, test_dataloader, class_names = \
        = create_dataloaders(train_dir=path/to/train_dir,
                             test_dir=path/to/test_dir,
                             transform=some_transform,
                             batch_size=32,
                             num_workers=4)
  """
  # Use ImageFolder to create dataset(s)
  train_data = datasets.ImageFolder(train_dir, transform=transform)
  test_data = datasets.ImageFolder(test_dir, transform=transform)

  # Get class names
  class_names = train_data.classes
  #Adding part where it takes just small amount of data
  
  train_size = 500
  train_extra_size = len(train_data) - train_size
  torch.manual_seed(42)
  train_ds, val_ds = random_split(train_data, [train_size, train_extra_size])
  
  test_size = 50
  test_extra_size = len(test_data) - test_size

  test_ds, test_val_ds = random_split(test_data, [test_size, test_extra_size])
  len(test_ds), len(test_val_ds)

  # Turn images into data loaders
  train_dataloader = DataLoader(
      train_ds,
      batch_size=batch_size,
      shuffle=True,
      num_workers=num_workers,
      pin_memory=True,
  )
  test_dataloader = DataLoader(
      test_ds,
      batch_size=batch_size,
      shuffle=False,
      num_workers=num_workers,
      pin_memory=True,
  )

  return train_dataloader, test_dataloader, class_names
