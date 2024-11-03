from tqdm import tqdm
import copy

from torch import optim
import torch

from .loss import correlation_coeff
from .models import VAE_classify, ae_ecv_loss_classify, vae_classify_loss, AutoencoderEquationsClassify, ae_ecv_loss_classify

#test_size = 1000
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def training_AE_C(train_dataloader, test_dataloader, latent_dims, unique_symbols, num_epochs, learning_rate, test_size, max_len, classes, weight):
    autoencoder_equations = AutoencoderEquationsClassify(latent_dims=latent_dims, num_symbols=len(unique_symbols), max_length=max_len, num_classes=len(classes)).to(device)
    # Optimizer
    optimizer = optim.Adam(autoencoder_equations.parameters(), lr=learning_rate)
    # Training loop
    train_losses = []
    test_losses = []
    correlations_cor = []
    correlations_dis = []
    correlations_dis_train = []
    test_reconstruction_losses = []
    test_constant_losses = []
    test_latent_correlation_losses = []
    best_accuracy = 0
    batch_correlation_cor = 0.0
    batch_correlation_dis = 0.0
    best_test_loss = 10000000
    # print(train_dataloader)
    for epoch in tqdm(range(num_epochs)):
        x_batches_current = []
        x_hat_batches_current = []
        # Training loop for the training set
        autoencoder_equations.train()
        for equations_batch, constant_list, values_batch in train_dataloader:
            optimizer.zero_grad()
            # constant_list = constant_list.unsqueeze(1).float()
            # Forward pass
            # recon_batch, mean, logvar = myvae(equations_batch)
            (recon_classes, recon_batch_constants), z = autoencoder_equations(
                equations_batch, constant_list
            )
            cls = [classes.index(eq.tolist()) for eq in equations_batch]
            loss, losses = ae_ecv_loss_classify(
                recon_classes,
                recon_batch_constants,
                values_batch,
                constant_list,
                cls, 
                z, 
                weight=weight
            )

            # Backward pass and optimization
            loss.backward()
            optimizer.step()

            correlation_cor, correlation_dis, _, _ = correlation_coeff(
                    values_batch[:, 1, :], z
                )
            batch_correlation_cor += correlation_cor
            batch_correlation_dis += float(correlation_dis)
        

        average_correlation_dis_train = batch_correlation_dis / len(train_dataloader)

        # Evaluation loop for the test set
        total_test_loss = 0.0
        batch_correlation_cor = 0.0
        batch_correlation_dis = 0.0
        test_reconstruction_loss = 0.0
        test_constant_loss = 0.0
        test_latent_correlation_loss = 0.0
        autoencoder_equations.eval()  # Set the model to evaluation mode
        with torch.no_grad():
            for test_equations_batch, constant_list, values_batch in test_dataloader:
                # constant_list = constant_list.unsqueeze(1).float()
                # Forward pass
                # recon_batch, mean, logvar = myvae(test_equations_batch)
                (recon_batch_syntax, recon_batch_constants), z = autoencoder_equations(
                    test_equations_batch, constant_list
                )

                cls =  [classes.index(eq.tolist()) for eq in test_equations_batch]
                test_loss, losses = ae_ecv_loss_classify(
                    recon_batch_syntax,
                    recon_batch_constants,
                    values_batch,
                    constant_list,
                    cls,
                    z

                )
                correlation_cor, correlation_dis, _, _ = correlation_coeff(
                    values_batch[:, 1, :], z
                )
                batch_correlation_cor += correlation_cor
                batch_correlation_dis += correlation_dis
                # Accumulate the loss over all test batches
                total_test_loss += test_loss.item() * test_equations_batch.size(0)
                test_reconstruction_loss += losses[0].item() * test_equations_batch.size(0)
                test_constant_loss += losses[1].item() * test_equations_batch.size(0)
                test_latent_correlation_loss += losses[2].item() * test_equations_batch.size(0)
                # Save the last batch reconstruction inputs and outputs
                #if epoch == num_epochs - 1:
                x_batches_current.append((test_equations_batch, constant_list))
                x_hat_batches_current.append((recon_batch_syntax, recon_batch_constants))
        

        average_test_loss = total_test_loss / test_size
        average_correlation_cor = batch_correlation_cor / len(test_dataloader)
        average_correlation_dis = batch_correlation_dis / len(test_dataloader)

        if  average_test_loss < best_test_loss or epoch == 1:
            final_model = copy.deepcopy(autoencoder_equations)
            best_correlation_dis = average_correlation_dis
            best_correlation_cor = average_correlation_cor
            best_test_loss = average_test_loss
            #best_accuracy = average_correlation_cor
            best_epoch = epoch
            x_batches = x_batches_current
            x_hat_batches = x_hat_batches_current

        # Print the loss for this epoch
        train_losses.append(loss.item())
        test_losses.append(average_test_loss)
        correlation_dis_train = batch_correlation_dis / len(train_dataloader)
        test_reconstruction_losses.append(test_reconstruction_loss / test_size)
        test_constant_losses.append(test_constant_loss / test_size)
        test_latent_correlation_losses.append(test_latent_correlation_loss / test_size)
        correlations_cor.append(average_correlation_cor)
        correlations_dis.append(average_correlation_dis)
        correlations_dis_train.append(average_correlation_dis_train)
        #print(
        #    f"Epoch {epoch + 1}/{num_epochs}, "
        #    f"Training Loss: {loss.item()}, Test Loss: {average_test_loss}, Correlation Cor: {average_correlation_cor}, Correlation Dis: {average_correlation_dis}"
        #)
    df_results ={}
    df_results['correlation_dis_best'] = best_correlation_dis
    df_results['test_reconstruction_loss'] = test_reconstruction_losses
    df_results['test_constant_loss'] = test_constant_losses
    df_results['test_latent_correlation_loss'] = test_latent_correlation_losses
    df_results['train_losses'] = train_losses
    df_results['test_losses'] = test_losses
    df_results['correlation_dis'] = correlations_dis
    df_results['x_batches'] = x_batches
    df_results['x_hat_batches'] = x_hat_batches
    autoencoder_equations = final_model
    return final_model, df_results



def training_VAE_C(train_dataloader, test_dataloader, latent_dims, unique_symbols, num_epochs, learning_rate, test_size, kl_weight, classes, max_len, weight): 

    autoencoder_equations = VAE_classify(latent_dims=latent_dims, num_classes=len(classes), num_symbols=len(unique_symbols), max_length=max_len, vocab_size=len(unique_symbols)).to(device)
    # Optimizer
    optimizer = optim.Adam(autoencoder_equations.parameters(), lr=learning_rate)
    # Training loop
    train_losses = []
    test_losses = []
    test_reconstruction_losses = []
    test_constant_losses = []
    test_latent_correlation_losses = []
    test_kl_divergences = []
    correlations_cor = []
    correlations_dis = []
    best_correlation_dis = 0
    best_test_loss = 1000000
    # print(train_dataloader)
    for epoch in tqdm(range(num_epochs)):
        x_batches_current = []
        x_hat_batches_current = []
        # Training loop for the training set
        autoencoder_equations.train()
        for equations_batch, constant_list, values_batch in train_dataloader:
            optimizer.zero_grad()
            # constant_list = constant_list.unsqueeze(1).float()
            # Forward pass
            # recon_batch, mean, logvar = myvae(equations_batch)
            (recon_batch_syntax, recon_batch_constants), z, mean, logvar = autoencoder_equations(
                equations_batch, constant_list
            )
            cls =  [classes.index(eq.tolist()) for eq in equations_batch]
            loss, _ = vae_classify_loss(
                recon_batch_syntax,
                recon_batch_constants,
                cls,
                constant_list,
                values_batch,
                z,
                mean,
                logvar, 
                kl_weight, 
                weight
            )

            # Backward pass and optimization
            loss.backward()
            optimizer.step()

        # Evaluation loop for the test set
        total_test_loss = 0.0
        test_reconstruction_loss = 0.0
        test_constant_loss = 0.0
        test_latent_correlation_loss = 0.0
        test_kl_divergence = 0.0
        batch_correlation_cor = 0.0
        batch_correlation_dis = 0.0
        autoencoder_equations.eval()  # Set the model to evaluation mode
        with torch.no_grad():
            for test_equations_batch, constant_list, values_batch in test_dataloader:
                # constant_list = constant_list.unsqueeze(1).float()
                # Forward pass
                # recon_batch, mean, logvar = myvae(test_equations_batch)
                (recon_batch_syntax, recon_batch_constants), z, mean, logvar = autoencoder_equations(
                    test_equations_batch, constant_list
                )
                cls =  [classes.index(eq.tolist()) for eq in test_equations_batch]
                test_loss, test_loss_individual = vae_classify_loss(
                    recon_batch_syntax,
                    recon_batch_constants,
                    cls,
                    constant_list,
                    values_batch,
                    z,
                    mean,
                    logvar, 
                    kl_weight,
                    weight
                )
                correlation_cor, correlation_dis, _, _ = correlation_coeff(
                    values_batch[:, 1, :], z
                )
                batch_correlation_cor += correlation_cor
                batch_correlation_dis += correlation_dis
                # Accumulate the loss over all test batches
                total_test_loss += test_loss.item() * test_equations_batch.size(0)
                test_reconstruction_loss += test_loss_individual[0].item() * test_equations_batch.size(0)
                test_constant_loss += test_loss_individual[1].item() * test_equations_batch.size(0)
                test_latent_correlation_loss += test_loss_individual[2].item() * test_equations_batch.size(0)
                test_kl_divergence += test_loss_individual[3].item() * test_equations_batch.size(0)
                # Save the last batch reconstruction inputs and outputs
                #if epoch == num_epochs - 1:
                x_batches_current.append((test_equations_batch, constant_list))
                x_hat_batches_current.append((recon_batch_syntax, recon_batch_constants))

        average_test_loss = total_test_loss / test_size
        average_correlation_cor = batch_correlation_cor / len(test_dataloader)
        average_correlation_dis = batch_correlation_dis / len(test_dataloader)
        if  average_test_loss < best_test_loss or epoch == 1:
            final_model = copy.deepcopy(autoencoder_equations)
            best_correlation_dis = average_correlation_dis
            best_correlation_cor = average_correlation_cor
            best_test_loss = average_test_loss
            best_accuracy = average_correlation_cor
            best_epoch = epoch
            x_batches = x_batches_current
            x_hat_batches = x_hat_batches_current

        # Print the loss for this epoch
        train_losses.append(loss.item())
        test_losses.append(average_test_loss)
        test_reconstruction_losses.append(test_reconstruction_loss / test_size)
        test_constant_losses.append(test_constant_loss / test_size)
        test_latent_correlation_losses.append(test_latent_correlation_loss / test_size)
        test_kl_divergences.append(test_kl_divergence / test_size)
        correlations_cor.append(average_correlation_cor)
        correlations_dis.append(average_correlation_dis)
        #print(
        #    f"Epoch {epoch + 1}/{num_epochs}, "
        #    f"Training Loss: {loss.item()}, Test Loss: {average_test_loss}, Correlation_cor: {average_correlation_cor}, Correlation_dis: {average_correlation_dis}"
        #)
    df_results ={}
    df_results['correlation_dis_best'] = best_correlation_dis
    #df_results['correlation_cor'] = best_correlation_cor
    df_results['test_reconstruction_loss'] = test_reconstruction_losses
    df_results['test_constant_loss'] = test_constant_losses
    df_results['test_latent_correlation_loss'] = test_latent_correlation_losses
    df_results['test_kl_divergence'] = test_kl_divergences
    df_results['train_losses'] = train_losses
    df_results['test_losses'] = test_losses
    df_results['correlation_dis'] = correlations_dis
    df_results['x_batches'] = x_batches
    df_results['x_hat_batches'] = x_hat_batches
    
    autoencoder_equations = final_model
    return final_model, df_results