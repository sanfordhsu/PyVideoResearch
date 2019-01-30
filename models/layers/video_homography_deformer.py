import torch
import torch.nn as nn
import torch.nn.functional as F


class VideoHomographyDeformer(nn.Module):
    def __init__(self, channels):
        super(VideoHomographyDeformer, self).__init__()
        self.theta = nn.Parameter(torch.Tensor(channels, 3 * 2))
        self.projection = nn.Parameter(torch.Tensor(channels, 3 * 1))
        identity = torch.Tensor([1, 0, 0, 0, 1, 0]).float()
        self.theta.data.copy_(identity[None, :].repeat(channels, 1))
        self.projection.data.zero_()

    def forward(self, x):
        conv3d = x.dim() == 5
        if conv3d:
            b, n, d, d, c = x.shape
            x = x.reshape(-1, d, d, c)
            x = x.permute(0, 3, 1, 2)
        theta = self.theta.view(-1, 2, 3)
        grid = F.affine_grid(theta, x.size())
        projection = self.projection.view(-1, 1, 3)
        projection[:, 0, 2] = 1
        projection = projection.repeat(1, 2, 1)
        grid_projection = F.affine_grid(projection, x.size())
        grid = grid / grid_projection
        x = F.grid_sample(x, grid, padding_mode="reflection")
        if conv3d:
            x = x.permute(0, 2, 3, 1)
            x = x.reshape(b, n, d, d, c)
        print('grid min: {} grid max: {} grid mean: {}'.format(grid.min(), grid.max(), grid.mean()))
        return x