import numpy as np
import matplotlib.pyplot as plt

def generate_ddpm_schedule(timesteps=50):
    beta_start, beta_end = 0.001, 0.02
    betas = np.linspace(beta_start, beta_end, timesteps)
    alphas = 1.0 - betas
    alphas_bar = np.cumprod(alphas, axis=0)
    return betas, alphas_bar

def simulate_production_diffusion(img_size=128, timesteps=50):
    betas, alphas_bar = generate_ddpm_schedule(timesteps)
    current_latent = np.random.normal(0, 1, (img_size, img_size))
    
    x = np.linspace(-1, 1, img_size)
    y = np.linspace(-1, 1, img_size)
    X, Y = np.meshgrid(x, y)
    sphere_prior = (1.0 - np.clip(np.sqrt(X**2 + Y**2), 0, 1) - 0.5) * 2.0

    display_steps = np.linspace(0, timesteps - 1, 5, dtype=int)
    fig, axes = plt.subplots(1, 5, figsize=(15, 3))
    ax_idx = 0
    
    for t in reversed(range(timesteps)):
        alpha = 1.0 - betas[t]
        alpha_bar = alphas_bar[t]
        sigma_t = np.sqrt(betas[t])
        
        eps_predicted = (current_latent - np.sqrt(alpha_bar) * sphere_prior) / np.sqrt(1 - alpha_bar)
        z = np.random.normal(0, 1, (img_size, img_size)) if t > 0 else 0
        current_latent = (1 / np.sqrt(alpha)) * (current_latent - (betas[t] / np.sqrt(1 - alpha_bar)) * eps_predicted) + sigma_t * z
        
        if t in display_steps:
            viewable_img = (current_latent - current_latent.min()) / (current_latent.max() - current_latent.min())
            axes[ax_idx].imshow(viewable_img, cmap='plasma')
            axes[ax_idx].set_title(f"Step {timesteps - t}")
            axes[ax_idx].axis('off')
            ax_idx += 1
            
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    simulate_production_diffusion()
